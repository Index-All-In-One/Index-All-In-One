import asyncio, re, os, sys, datetime
from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, Message

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from opensearch.conn import OpenSearch_Conn

from plugins.status_code import PluginReturnStatus
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

API_ID = 27390216
API_HASH = 'b59c778394e993b6bb4a1b8ada427520'

class Telegram_Instance:
    def __init__(self, plugin_instance_id, phone_number, password=None):

        self.plugin_instance_id = plugin_instance_id
        self.phone_number = phone_number
        self.password = password

        self.client = TelegramClient(self.plugin_instance_id, API_ID, API_HASH)
        self.opensearch_conn = OpenSearch_Conn()
        

    def login_opensearch(self, host='localhost', port=9200, username='admin', password='admin',
use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):

        try:
            self.opensearch_conn.connect(host, port, username, password,
        use_ssl, verify_certs, ssl_assert_hostname, ssl_show_warn)
            logging.debug("Opensearch login success.")
        except:
            logging.debug("Opensearch login failed.")

    async def login_telegram(self, two_step_code=None):
        try:
            # self.client = TelegramClient(self.plugin_instance_id, self.api_id, self.api_hash)
            if two_step_code and not await self.client.is_user_authorized():
                await self.client.sign_in(phone=self.phone_number, code=two_step_code)

            else:
                await self.client.start(self.phone_number)

            logging.debug("Logged in Telegram as {}!".format(self.phone_number))
            return True
        except:
            logging.debug("Telegram login failed.")
            return False

    async def disconnect_telegram(self):
        await self.client.disconnect()

    async def get_messages(self):

        # Iterate over all the dialogs and print the title and ID of each chat
        messages = []
        doc_ids = []
        logging.debug(f'Telegram plugin instance {self.plugin_instance_id} get_messages')
        async for dialog in self.client.iter_dialogs():
            if dialog.is_group:
                conv_type = 'Group'
            elif dialog.is_channel:
                conv_type = 'Channel'
            else:
                # print(f'Private chat: {dialog.title} (ID: {dialog.id})')
                conv_type = 'private chat'

            dialog_title = dialog.title
            dialog_id = dialog.entity.id
            dialog_name = dialog.name
            
            async for message in self.client.iter_messages(dialog_id):
                if isinstance(message, Message):
                    # doc_id
                    message_id = message.id
                    # print(message_id)
                    doc_id = str(dialog_id) + "_" + str(message_id)
                    # doc_name
                    sender = await message.get_sender()
                    
                    sender_name = "{} {}".format(sender.first_name, sender.last_name if sender.last_name else "")
                    doc_name = sender_name

                    # print(sender_name)
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
        print("YESS")
        doc_ids, messages = await self.get_messages()
        print("\nupdate_messages\n")
        ops_doc_ids = self.opensearch_conn.get_doc_ids(plugin_instance_id=self.plugin_instance_id)
        # if doc in OpenSearch but not in mailbox, delete doc
        _, doc_ids_to_be_delete = self.not_in(ops_doc_ids, doc_ids)

        for doc_id in doc_ids_to_be_delete:
            response = self.opensearch_conn.delete_doc(doc_id=doc_id,plugin_instance_id=self.plugin_instance_id)

        # if doc in telegram but not in OpenSearch, insert doc
        mask, doc_ids_to_be_insert = self.not_in(doc_ids, ops_doc_ids)

        
        messages = [messages[i] for i in range(len(mask)) if not mask[i]]
        for i in range(len(messages)):
            response = self.opensearch_conn.insert_doc(messages[i])

    def not_in(self, list1, list2):
        ''' return items in list1 that do not exist in list2 '''
        mask = [item in list2 for item in list1]
        res = [list1[i] for i in range(len(mask)) if not mask[i]]
        return mask, res
    
    async def send_code(self):
        await self.client.connect()
        await self.client.send_code_request(self.phone_number)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm, Column, Integer, String

model = orm.declarative_base()
DB_NAME = "p_telegram.db"

class TelegramCredentials(model):
    __tablename__ = 'telegram_credentials'

    id = Column(Integer, primary_key=True)
    plugin_instance_id = Column(String(50), nullable=True)
    phone_number = Column(String(50), nullable=False)

    def __init__(self, plugin_instance_id, phone_number):
        self.plugin_instance_id = plugin_instance_id
        self.phone_number = phone_number

def plugin_telegram_init(plugin_instance_id, plugin_init_info):
    
    # add credentials of plugin instance
    phone_number = plugin_init_info["phone_number"]
    password = None
    if password in plugin_init_info:
        password = plugin_init_info["password"]
    TelegramSession = Telegram_Instance(plugin_instance_id, phone_number, password)
    
    # two step plugin, step 1 send_code
    if "two_step_code" not in plugin_init_info:
        asyncio.run(TelegramSession.send_code())
        return PluginReturnStatus.NEED_TWO_STEP_CODE    

    # two step plugin, step 2 login
    two_step_code = plugin_init_info["two_step_code"]
    status = asyncio.run(TelegramSession.login_telegram(two_step_code))

    if not status:
        logging.error(f'init telegram plugin instance {plugin_instance_id} failed, wrong credentials')
        return PluginReturnStatus.EXCEPTION
    else:
        asyncio.run(TelegramSession.disconnect_telegram())

    # create an engine that connects to the database
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    model.metadata.bind = engine
    model.metadata.create_all(engine)
    # create a session factory that uses the engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # create a new TelegramCredential object and add it to the database
    plugin_instance_credentials = TelegramCredentials(plugin_instance_id, API_ID, API_HASH, phone_number)
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

    logging.debug(f'Telegram plugin instance {plugin_instance_id} updating, db name: {DB_NAME}')
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # get credential of plugin_instance_id
    creds = session.query(TelegramCredentials).filter(TelegramCredentials.plugin_instance_id==plugin_instance_id).first()
    session.commit()
    # login
    phone_number = creds.phone_number
    password = creds.password

    TelegramSession = Telegram_Instance(plugin_instance_id, phone_number, password)
    
    asyncio.run(TelegramSession.login_telegram())
    TelegramSession.login_opensearch(host=opensearch_hostname)
    print("\nHELLO3\n")
    asyncio.run(TelegramSession.update_messages())
    print("\nHELLO5\n")
    asyncio.run(TelegramSession.disconnect_telegram())
    return PluginReturnStatus.SUCCESS

def plugin_telegram_info_def():
    return PluginReturnStatus.SUCCESS, {"hint": "Please enter your api_idand api_hash. If you don't have one, create one first.", \
            "field_def": [\
                {
                    "field_name": "phone_number", \
                    "display_name": "phone_number", \
                    "type": "text",
                }, \
                {
                    "field_name": "password", \
                    "display_name": "Password", \
                    "type": "secret",
                }, \
                {
                    "field_name": "two_step_code", \
                    "display_name": "2FA Code", \
                    "type": "two_step",
                }, \
            ],}

async def main():

    phone_number = '+18056375418'

    # Create a new Telegram_Instance and start it
    TelegramSession = Telegram_Instance('1', phone_number)
    TelegramSession.login_opensearch()
    await TelegramSession.login_telegram()
    # Display the messages in the chat
    _, messages =  await TelegramSession.get_messages()
    print(messages)

    await TelegramSession.update_messages()
    await TelegramSession.client.disconnect()
# Run the async function
asyncio.run(main())
