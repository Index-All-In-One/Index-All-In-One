import asyncio, re, os, sys, datetime
from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, Message

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from opensearch.conn import OpenSearch_Conn

from plugins.status_code import PluginReturnStatus
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class Telegram_Instance:
    def __init__(self, plugin_instance_id, api_id, api_hash, phone_number):
        self.plugin_instance_id = plugin_instance_id
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number

        self.client = TelegramClient('main', api_id, api_hash)
        self.opensearch_conn = OpenSearch_Conn()

    def login_opensearch(self, host='localhost', port=9200, username='admin', password='admin',
use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):

        try:
            self.opensearch_conn.connect(host, port, username, password,
        use_ssl, verify_certs, ssl_assert_hostname, ssl_show_warn)
            print("Opensearch login success.")
        except:
            print("Opensearch login failed.")

    async def login_telegram(self):
        try:
            await self.client.start(self.phone_number)
            logging.debug("Logged in as {}!".format(self.user))
            return True
        except:
            logging.debug("Email login failed.")
            return False


    async def get_messages(self):

        # Iterate over all the dialogs and print the title and ID of each chat
        messages = []
        doc_ids = []
        async for dialog in self.client.iter_dialogs():
            if dialog.is_group:
                print(f'Group: {dialog.title} (ID: {dialog.id})')
                conv_type = 'Group'
            elif dialog.is_channel:
                print(f'Channel: {dialog.title} (ID: {dialog.id})')
                conv_type = 'Channel'
            else:
                print(f'Private chat: {dialog.title} (ID: {dialog.id})')
                conv_type = 'private chat'

            # if isinstance(dialog.entity, PeerUser):
            #     conv_type = 'user'
            # elif isinstance(dialog.entity, PeerChat):
            #     conv_type = 'chat'
            # elif isinstance(dialog.entity, PeerChannel):
            #     conv_type = 'channel'

            dialog_id = dialog.entity.id
            dialog_name = dialog.name
            
            async for message in self.client.iter_messages(dialog_id):
                if isinstance(message, Message):
                    # doc_id
                    message_id = message.id
                    doc_id = str(dialog_id) + "_" + str(message_id)
                    # doc_name
                    # sender = await self.client.get_entity(message.from_id); sender_name = "{} {}".format(sender.first_name, sender.last_name)
                    sender = await self.client.get_entity(message.from_id); sender_name = "{} {}".format(sender.first_name, sender.last_name)
                    doc_name = sender_name
                    # link
                    link = ""
                    if dialog.is_group:
                        link = "https://t.me/c/{}/{}".format(dialog_id, message_id)
                    elif dialog.is_channel:
                        link = ""
                    else:
                        link = "https://web.telegram.org/z/#{}".format(dialog_id)
                    # created_date
                    created_date = message.date.strftime('%Y-%m-%dT%H:%M:%SZ')
                    # modified_date
                    modified_date = message.date.strftime('%Y-%m-%dT%H:%M:%SZ')
                    if message.edit_date is not None:
                        modified_date = message.edit_date.strftime('%Y-%m-%dT%H:%M:%SZ')
                    # content
                    content = message.message
                    # summary
                    summary = "Dialog: {}, Type: {}, Sender: {}".format(dialog_name, conv_type, sender_name)
                    # file_size
                    file_size = len(message.raw_text.encode('utf-8'))
                    
                    body = {
                        "doc_id": doc_id,
                        "doc_name": doc_name,
                        "doc_type": 'Telegram',
                        "link": link,
                        "created_date": created_date,
                        "modified_date": modified_date,
                        "summary": summary,
                        "file_size": int(file_size),
                        "plugin_instance_id": self.plugin_instance_id,
                        "content": content
                    }
                    doc_ids.append(doc_id)
                    messages.append(body)

        return doc_ids, messages
                    
    async def update_messages(self):
        doc_ids, messages = await self.get_messages()
        print(doc_ids)

        ops_doc_ids = self.opensearch_conn.get_doc_ids(plugin_instance_id=self.plugin_instance_id)
        # if doc in OpenSearch but not in mailbox, delete doc
        _, doc_ids_to_be_delete = self.not_in(ops_doc_ids, doc_ids)
        for doc_id in doc_ids_to_be_delete:
            response = self.opensearch_conn.delete_doc(doc_id=doc_id,plugin_instance_id=self.plugin_instance_id)

        # if doc in telegram but not in OpenSearch, insert doc
        mask, doc_ids_to_be_insert = self.not_in(doc_ids, ops_doc_ids)
        print(mask)
        messages = [messages[i] for i in range(len(mask)) if not mask[i]]
        for i in range(len(messages)):
            response = self.opensearch_conn.insert_doc(messages[i])

    def not_in(self, list1, list2):
        ''' return items in list1 that do not exist in list2 '''
        mask = [item in list2 for item in list1]
        res = [list1[i] for i in range(len(mask)) if not mask[i]]
        return mask, res


    # async def get_message_info(self, dialog_id, message_id):
    #     entity = await self.client.get_entity(dialog_id)
    #     message = await self.client.get_messages(entity, ids=message_id)
    #     link = await self.client.get_message_link(entity, message)
    #     return {
    #         'id': message.id,
    #         'sender': message.sender_id,
    #         'content': message.message,
    #         'size': message.file.size if message.file else 0,
    #         'link': link
    #     }


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm, Column, Integer, String

model = orm.declarative_base()
DB_NAME = "p_telegram.db"
class TelegramCredentials(model):
    __tablename__ = 'telegram_credentials'

    id = Column(Integer, primary_key=True)
    plugin_instance_id = Column(String(50), nullable=True)
    api_id = Column(String(50), nullable=False)
    api_hash = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False)

    def __init__(self, plugin_instance_id, api_id, api_hash, phone_number):
        self.plugin_instance_id = plugin_instance_id
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number


def plugin_telegram_init(plugin_instance_id, plugin_init_info):

    # add credentials of plugin instance
    api_id = plugin_init_info["api_id"]
    api_hash = plugin_init_info["api_hash"]
    phone_number = plugin_init_info["phone_number"]
    # check if credentials correct
    TelegramSession = Telegram_Instance(plugin_instance_id, api_id, api_hash, phone_number)
    # status = TelegramSession.login_email()
    # if not status:
    #     logging.error(f'init telegram plugin instance {plugin_instance_id} failed, wrong credentials')
    #     return PluginReturnStatus.EXCEPTION

    # create an engine that connects to the database
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    model.metadata.bind = engine
    model.metadata.create_all(engine)
    # create a session factory that uses the engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # create a new TelegramCredential object and add it to the database
    plugin_instance_credentials = TelegramCredentials(plugin_instance_id, api_id, api_hash, phone_number)
    session.add(plugin_instance_credentials)
    session.commit()

    logging.info(f'Telegram plugin instance {plugin_instance_id} initialized, db name: {DB_NAME}')
    return PluginReturnStatus.SUCCESS


def plugin_telegram_del(plugin_instance_id):
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # delete the source
    creds = session.query(TelegramCredentials).filter_by(plugin_instance_id=plugin_instance_id).first()
    session.delete(creds)
    session.commit()
    return PluginReturnStatus.SUCCESS

def plugin_telegram_update(plugin_instance_id, opensearch_hostname='localhost'):
    logging.debug(f'Gmail plugin instance {plugin_instance_id} updating, db name: {DB_NAME}')
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # get credential of plugin_instance_id
    creds = session.query(TelegramCredentials).filter(TelegramCredentials.plugin_instance_id==plugin_instance_id).first()
    session.commit()
    # login
    api_id = creds.api_id
    api_hash = creds.api_hash
    phone_number = creds.phone_number

    TelegramSession = Telegram_Instance(plugin_instance_id, api_id, api_hash, phone_number)
    # TelegramSession.login_email()
    # TelegramSession.login_opensearch(host=opensearch_hostname)
    # TelegramSession.update_email()
    return PluginReturnStatus.SUCCESS

def plugin_telegram_info_def():
    return PluginReturnStatus.SUCCESS, {"hint": "Please enter your api_idand api_hash. If you don't have one, create one first.", \
            "field_def": [\
                { \
                    "field_name": "api_id", \
                    "display_name": "api_id", \
                    "type": "secret",
                }, \
                {
                    "field_name": "api_hash", \
                    "display_name": "api_hash", \
                    "type": "secret",
                }, \
                {
                    "field_name": "phone_number", \
                    "display_name": "phone_number", \
                    "type": "text",
                }, \
            ],}

async def main():
    api_id = 27390216
    api_hash = 'b59c778394e993b6bb4a1b8ada427520'
    phone_number = '+18056375418'

    # Create a new Telegram_Instance and start it
    TelegramSession = Telegram_Instance('1',api_id, api_hash, phone_number)
    TelegramSession.login_opensearch()
    await TelegramSession.login_telegram()
    # Display the messages in the chat
    # _, messages =  await TelegramSession.get_messages()
    # print(messages)

    await TelegramSession.update_messages()

# Run the async function
asyncio.run(main())
