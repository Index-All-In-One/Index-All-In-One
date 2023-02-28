import imaplib, email
import re, time
from opensearch_conn import *

IMAP_URL = 'imap.gmail.com'

class Gmail:
    def __init__(self, username, password):
        self.user = username
        self.password = password
        self.imap = None
        self.opensearch_conn = OpenSearch_Conn()

    def login_opensearch(self, host='localhost', port=9200, username='admin', password='admin', 
use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):
        
        try:
            self.opensearch_conn.connect(host, port, username, password,
        use_ssl, verify_certs, ssl_assert_hostname, ssl_show_warn)
        except:
            print("Opensearch log in failed.")

    def login_imap(self):
        try:
            self.imap = imaplib.IMAP4_SSL(IMAP_URL)
            self.imap.login(self.user, self.password)
            print("Logged in as {}!".format(self.user))
        except:
            print("Log in failed.")

    def get_emails(self, mailbox="Inbox"):
        '''
            Get the niversial id, content, and size of all emails in mailbox
        '''
        self.imap.select(mailbox)
        success, message_uids = self.imap.search(None, 'ALL')
        if not success: raise Exception("Email search Failed")
        message_uids = message_uids[0].split()

        doc_ids, messages, sizes = [], [], []
        for num in message_uids:
            # the universial id of email
            _, doc_id = self.imap.fetch(num, '(X-GM-MSGID)')
            doc_id = re.search(r'X-GM-MSGID (\d+)', doc_id[0].decode('utf-8')).group(1)
            # the content of email
            _, message = self.imap.fetch(num, '(RFC822)')
            # the size of email
            _, size = self.imap.fetch(num, '(RFC822.SIZE)')

            doc_ids.append(doc_id)
            messages.append(message)
            sizes.append(size)

        return doc_ids, messages, sizes

    def update_email(self):
        '''
            Update Opensearch index, delete documents not in inbox
        '''
        assert(self.imap)
        assert(self.opensearch_conn)

        inbox_doc_ids, messages, sizes = self.get_emails()
        existing_doc_ids = self.opensearch_conn.get_doc_ids(source=USER)

        _, doc_ids_to_be_delete = not_in(existing_doc_ids, inbox_doc_ids)
        mask, doc_ids_to_be_insert = not_in(inbox_doc_ids, existing_doc_ids)

        docs_to_be_insert = [messages[i] for i in range(len(mask)) if not mask[i]]
        sizes_to_be_insert = [sizes[i] for i in range(len(mask)) if not mask[i]]

        for doc_id in doc_ids_to_be_delete:
            keyword = {"match": {"doc_id": doc_id}}
            response = self.opensearch_conn.delete_doc(keyword)

        for i in range(len(doc_ids_to_be_insert)):
            body = self.to_opensearch_insert_format(doc_ids_to_be_insert[i], docs_to_be_insert[i],
                                        sizes_to_be_insert[i])
            
            response = self.opensearch_conn.insert_doc(body)


    def to_opensearch_insert_format(self, doc_id, message, size):
        message = email.message_from_bytes(message[0][1])

        title = message.get('Subject')
        gmail_url = f'https://mail.google.com/mail/u/0/#inbox/'
        send_date = message.get('Date')
        sender = message.get('From')
        receiver = message.get('To')
        bcc = message.get('BCC')
        size = re.search(r'RFC822.SIZE (\d+)', size[0].decode('utf-8')).group(1)
        # text_content = ''
        # for part in message.walk():
        #     if part.get_content_type() == "text/plain":
        #         text_content = part.get_payload(decode=True).decode('utf-8')

        body = {
            "doc_id": doc_id,
            "doc_name": title,
            "doc_type": 'Email',
            "link": gmail_url,
            "source": self.user,
            "created_date": None,
            "modified_date": None,
            "summary": "Sender: {}  Receiver: {}  BCC: {}".format(sender, receiver, bcc),
            "file_size": int(size)
        }
        return body


def not_in(list1, list2):
    ''' return items in list1 that do not exist in list2 '''
    mask = [item in list2 for item in list1]
    res = [list1[i] for i in range(len(mask)) if not mask[i]]
    return mask, res

# def plugin_gmail(email_username, email_password, host='localhost', port=9200, username='admin', password='admin', 
# use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):
#     gmail_conn = Gmail(email_username, email_password)
#     gmail_conn.opensearch_conn(host, port, username, password,use_ssl,verify_certs,ssl_assert_hostname,ssl_show_warn)




def plugin_gmail_update(plugin_instance_id):
    print("Plugin gmail update: ", plugin_instance_id)

def plugin_gmail_init(plugin_instance_id, plugin_init_info):
    print("Plugin gmail init: ", plugin_instance_id, plugin_init_info)

def plugin_gmail_del(plugin_instance_id):
    print("Plugin gmail del: ", plugin_instance_id)
