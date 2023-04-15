import asyncio, re, os, sys, datetime
from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, Message

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from opensearch.conn import OpenSearch_Conn

import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class Telegram_Instance:
    def __init__(self, plugin_instance_id, api_id, api_hash, phone_number):
        self.plugin_instance_id = plugin_instance_id
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('main', api_id, api_hash)
        self.phone_number = phone_number
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
        async for dialog in self.client.iter_dialogs():
            if dialog.is_group:
                print(f'Group: {dialog.title} (ID: {dialog.id})')
            elif dialog.is_channel:
                print(f'Channel: {dialog.title} (ID: {dialog.id})')
            else:
                print(f'Private chat: {dialog.title} (ID: {dialog.id})')
            # if isinstance(dialog.entity, PeerUser):
            #     conv_type = 'user'
            # elif isinstance(dialog.entity, PeerChat):
            #     conv_type = 'chat'
            # elif isinstance(dialog.entity, PeerChannel):
            #     conv_type = 'channel'

            dialog_id = dialog.entity.id
            dialog_name = dialog.name

            # print("dialog_id: " + str(dialog_id))
            async for message in self.client.iter_messages(dialog_id):
                if isinstance(message, Message):
                    message_id = message.id; doc_id = str(dialog_id) + "_" + str(message)
                    sender_id = message.from_id; doc_name = sender_id

                    link = "https://t.me/c/{}/{}".format(dialog_id, message_id)
                    created_date = message.date
                    modified_date = message.date
                    content = message.message
                    # summary = content
                    file_size = len(message.raw_text.encode('utf-8'))
                    
                    # print(f"Message ID: {message_id}, Sender ID: {sender_id}, Content: {content}, Size: {message_size}")

                body = {
                    "doc_id": doc_id,
                    "doc_name": doc_name,
                    "doc_type": 'Email',
                    "link": link,
                    "created_date": created_date,
                    "modified_date": modified_date,
                    "summary": "Dialog: {}, Sender: {}".format(dialog_name, sender_id),
                    "file_size": int(file_size),
                    "plugin_instance_id": self.plugin_instance_id,
                    "content": content
                }
                messages.append(body)
                print(body)
        # print(messages)
        return messages
                    
    # def update_messages(self):
    #     messages = self.get_messages()
    #     for m in messages:
    #         print(m)
    #         print()







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

# def plugin_gmail_info_def():
#     return PluginReturnStatus.SUCCESS, {"hint": "Please enter your app password, not Gmail's login password. If you don't have, create one first.", \
#             "field_def": [\
#                 { \
#                     "field_name": "username", \
#                     "display_name": "Username", \
#                     "type": "text",
#                 }, \
#                 {
#                     "field_name": "password", \
#                     "display_name": "Password", \
#                     "type": "secret",
#                 }, \
#             ],}

async def main():
    api_id = 27390216
    api_hash = 'b59c778394e993b6bb4a1b8ada427520'
    phone_number = '+18056375418'

    # Create a new Telegram_Instance and start it
    telegram = Telegram_Instance('1',api_id, api_hash, phone_number)
    await telegram.login_telegram()

    # Display the messages in the chat
    await telegram.get_messages()

    await telegram.update_messages()

# Run the async function
asyncio.run(main())
