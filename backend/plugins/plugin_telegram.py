import asyncio, re, os, sys, datetime
from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, Message, Channel, InputPeerChannel
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from opensearch.conn import OpenSearch_Conn

from plugins.status_code import PluginReturnStatus
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

API_ID = 27390216
API_HASH = 'b59c778394e993b6bb4a1b8ada427520'
DIR_NAME = "instance/telegram_sessions"

class Telegram_Instance:
    def __init__(self, plugin_instance_id, phone_number, password=None):
        self.plugin_instance_id = plugin_instance_id
        self.phone_number = phone_number
        self.password = password
        self.opensearch_conn = OpenSearch_Conn()
        self.client = None

    def login_opensearch(self, host='localhost', port=9200, username='admin', password='admin',
use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):

        try:
            self.opensearch_conn.connect(host, port, username, password,
        use_ssl, verify_certs, ssl_assert_hostname, ssl_show_warn)
            logging.debug("Opensearch login success.")
        except:
            logging.debug("Opensearch login failed.")

    async def connect_telegram(self):
        session_name = DIR_NAME + "/" + self.plugin_instance_id

        if not os.path.exists(DIR_NAME):
            os.makedirs(DIR_NAME)
        if os.path.exists(session_name):
            os.remove(session_name)

        if not self.client:
            self.client = TelegramClient(session_name, API_ID, API_HASH)

        await self.client.connect()

    async def disconnect_telegram(self):
        await self.client.disconnect()

    async def start_telegram(self, two_step_code=None):
        assert(self.client)

        try:
            # self.client = TelegramClient(self.plugin_instance_id, self.api_id, self.api_hash)
            if two_step_code:
                await self.client.start(self.phone_number, code_callback=lambda: two_step_code, password=self.password)

            elif await self.client.is_user_authorized():
                await self.client.start(self.phone_number)

            else:
                logging.debug("Telegram login failed.")
                return False

            logging.debug("Logged in Telegram as {}!".format(self.phone_number))
            return True
        except:
            logging.debug("Telegram login failed.")
            return False

    async def send_code(self):
        try:
            logging.info("Before send code, client.is_connected(): {}".format(self.client.is_connected()))
            await self.client.send_code_request(self.phone_number)
            logging.info("Code sent")
        except Exception as e:
            logging.error("Failed to send code, error {}".format(e))

    async def get_messages(self):

        # Iterate over all the dialogs and print the title and ID of each chat
        messages = []
        doc_ids = []
        sender_cache = {}
        logging.debug(f'Telegram plugin instance {self.plugin_instance_id} get_messages')
        async for dialog in self.client.iter_dialogs():

            if dialog.is_group:
                conv_type = 'Group'
            elif dialog.is_channel:
                conv_type = 'Channel'
            else:
                conv_type = 'Private Chat'

            dialog_title = dialog.title
            dialog_id = dialog.entity.id
            dialog_name = dialog.name

            limit = 100
            offset_id = 0
            max_id = 0
            min_id = 0
            add_offset = 0
            all_messages = []

            while True:
                history = await self.client(GetHistoryRequest(
                    peer=dialog_id,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=add_offset,
                    limit=limit,
                    max_id=max_id,
                    min_id=min_id,
                    hash=0
                ))

                if not history.messages:
                    break

                all_messages.extend(history.messages)
                offset_id = history.messages[-1].id
                await asyncio.sleep(1)  # Adding a small delay to avoid hitting rate limits

            for message in all_messages:
                if isinstance(message, Message):
                    # TODO: support more message type
                    if message.message:
                        # doc_id
                        message_id = message.id
                        if dialog.is_group or dialog.is_channel:
                            doc_id = "-" + str(dialog_id) + "_" + str(message_id)
                        else:
                            doc_id = str(dialog_id) + "_" + str(message_id)
                        # doc_name
                        doc_name = dialog_name
                        # link & doc_name
                        link = ""
                        dialog_public_name = getattr(dialog.entity, 'username', None)
                        if dialog.is_group:
                            chat = await self.client.get_entity(message.peer_id)
                            if isinstance(chat, Channel) and chat.megagroup:
                                if dialog_public_name:
                                    link = "https://t.me/{}/{}".format(dialog_public_name, message_id)
                                else:
                                    link = "https://t.me/c/{}/{}".format(dialog_id, message_id)
                            else:
                                if chat.migrated_to:
                                    supergroup = await self.client.get_entity(InputPeerChannel(chat.migrated_to.channel_id, chat.migrated_to.access_hash))
                                    doc_name = supergroup.title

                                if dialog_public_name:
                                    link = "https://t.me/{}".format(dialog_public_name)
                                else:
                                    link = "https://web.telegram.org/a/#-{}".format(dialog_id)

                        elif dialog.is_channel:
                            if dialog_public_name:
                                link = "https://t.me/{}/{}".format(dialog_public_name, message_id)
                            else:
                                link = "https://t.me/c/{}/{}".format(dialog_id, message_id)
                        else:
                            if dialog_public_name:
                                link = "https://t.me/{}".format(dialog_public_name)
                            else:
                                link = "https://web.telegram.org/a/#{}".format(dialog_id)

                        # created_date
                        created_date = message.date.strftime('%Y-%m-%dT%H:%M:%SZ')
                        # modified_date
                        modified_date = message.date.strftime('%Y-%m-%dT%H:%M:%SZ')
                        if message.edit_date is not None:
                            modified_date = message.edit_date.strftime('%Y-%m-%dT%H:%M:%SZ')
                        # content
                        content = message.message
                        # summary
                        sender_name = ""
                        if dialog.is_channel or message.from_id is None:
                            sender_name = ""
                        else:
                            sender_id = message.from_id.user_id
                            if sender_id not in sender_cache:
                                sender = await message.get_sender()
                                sender_cache[sender_id] = sender
                                await asyncio.sleep(0.04)
                            else:
                                sender = sender_cache[sender_id]
                            if sender is not None:
                                sender_name = "{} {}".format(sender.first_name, sender.last_name if sender.last_name else "")
                            else:
                                sender_name = ""

                        content_summary = content[:600] + '...' if len(content) > 600 else content
                        summary = "Dialog: {}, Type: {}, Sender: {},\nMessage:\n{}".format(dialog_name, conv_type, sender_name, content_summary)
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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm, Column, Integer, String

model = orm.declarative_base()
DB_NAME = "p_telegram.db"

class TelegramCredentials(model):
    __tablename__ = 'telegram_credentials'

    id = Column(Integer, primary_key=True)
    plugin_instance_id = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False)
    password = Column(String(50), nullable=True)

    def __init__(self, plugin_instance_id, phone_number, password=None):
        self.plugin_instance_id = plugin_instance_id
        self.phone_number = phone_number
        self.password = password

def plugin_telegram_init(plugin_instance_id, plugin_init_info):

    async def init(TelegramSession: Telegram_Instance, code=None):
        status = None
        await TelegramSession.connect_telegram()
        if not code:
            await TelegramSession.send_code()
        else:
            status = await TelegramSession.start_telegram(code)
        await TelegramSession.disconnect_telegram()

        return status

    # Create the directory if it doesn't exist
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)

    # add credentials of plugin instance
    phone_number = plugin_init_info["phone_number"]
    password = plugin_init_info["password"]
    if password=="":
        password = None
    TelegramSession = Telegram_Instance(plugin_instance_id, phone_number, password)

    # two step plugin, step 1 send_code
    if "two_step_code" not in plugin_init_info:
        logging.info(f'Telegram plugin instance {plugin_instance_id} send code')
        asyncio.run(init(TelegramSession))
        return PluginReturnStatus.NEED_TWO_STEP_CODE

    # two step plugin, step 2 login
    two_step_code = plugin_init_info["two_step_code"]
    status = asyncio.run(init(TelegramSession, two_step_code))

    if not status:
        logging.error(f'init telegram plugin instance {plugin_instance_id} failed, wrong credentials')
        return PluginReturnStatus.EXCEPTION

    # create an engine that connects to the database
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    model.metadata.bind = engine
    model.metadata.create_all(engine)
    # create a session factory that uses the engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # create a new TelegramCredential object and add it to the database
    plugin_instance_credentials = TelegramCredentials(plugin_instance_id, phone_number, password)
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
    async def update(TelegramSession):
        await TelegramSession.connect_telegram()
        await TelegramSession.start_telegram()
        await TelegramSession.update_messages()
        await TelegramSession.disconnect_telegram()

    logging.debug(f'Telegram plugin instance {plugin_instance_id} updating, db name: {DB_NAME}')
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # get credential of plugin_instance_id
    creds = session.query(TelegramCredentials).filter(TelegramCredentials.plugin_instance_id==plugin_instance_id).first()
    session.commit()
    phone_number = creds.phone_number
    password = creds.password

    # update
    TelegramSession = Telegram_Instance(plugin_instance_id, phone_number, password)
    TelegramSession.login_opensearch(host=opensearch_hostname)
    asyncio.run(update(TelegramSession))

    return PluginReturnStatus.SUCCESS

def plugin_telegram_info_def():
    return PluginReturnStatus.SUCCESS, {"hint": "If you have ever set a password, you need to enter it; otherwise, you don't need to input it.", \
            "field_def": [\
                {
                    "field_name": "phone_number", \
                    "display_name": "phone_number", \
                    "type": "text",
                }, \
                {
                    "field_name": "two_step_code", \
                    "display_name": "2FA Code", \
                    "type": "two_step",
                }, \
                {
                    "field_name": "password", \
                    "display_name": "Password (Conditional)", \
                    "type": "secret_opt",
                }, \
            ],}


async def test1():

    phone_number = '+18056375418'
    # Create the directory if it doesn't exist
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)

    client = TelegramClient( DIR_NAME + "/1", API_ID, API_HASH)
    await client.connect()
    await client.send_code_request(phone_number)
    await client.disconnect()

async def test2():
    phone_number = '+18056375418'
    code = 92200
    # hash = 'f54fb2b6589a19ede2'

    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)

    client = TelegramClient( DIR_NAME + "/1", API_ID, API_HASH)
    await client.connect()
    await client.start(phone_number, code_callback=lambda: code)
    await client.log_out()
    await client.disconnect()

async def test3():
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)

    plugin_instance_id = "1"
    phone_number = '+18056375418'
    TelegramSession = Telegram_Instance(plugin_instance_id, phone_number)
    await TelegramSession.connect_telegram()
    await TelegramSession.send_code()
    await TelegramSession.disconnect_telegram()

    return 0

async def test4():
    plugin_instance_id = "1"
    phone_number = '+18056375418'
    code = 89365

    TelegramSession = Telegram_Instance(plugin_instance_id, phone_number)
    await TelegramSession.connect_telegram()
    await TelegramSession.start_telegram(code)
    res = await TelegramSession.get_messages()
    await TelegramSession.disconnect_telegram()

    return res

if __name__ == "__main__":
    # asyncio.run(test1())
    # asyncio.run(test2())
    # asyncio.run(test3())
    res = asyncio.run(test4())
    print(res)
