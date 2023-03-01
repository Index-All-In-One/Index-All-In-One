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

    def login(self):
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

        doc_ids, doc_content, doc_sizes = [], [], []
        for num in message_uids:
            # the universial id of email
            _, doc_id = self.imap.fetch(num, '(X-GM-MSGID)')
            doc_id = re.search(r'X-GM-MSGID (\d+)', doc_id[0].decode('utf-8')).group(1)
            # the content of email
            _, message = self.imap.fetch(num, '(RFC822)')
            # the size of email
            _, size = self.imap.fetch(num, '(RFC822.SIZE)')

            doc_ids.append(doc_id)
            doc_content.append(message)
            doc_sizes.append(size)

        return doc_ids, doc_content, doc_sizes

    def update_email(self):
        '''
            Update OpenSearch index, delete documents in OpenSearch but not in mailbox, 
            insert documents new in mailbox but not in OpenSearch
        '''
        assert(self.imap)
        assert(self.opensearch_conn)

        # get all emails from mailbox
        mailbox_doc_ids, doc_content, doc_sizes = self.get_emails()
        # get all emails from OpenSearch
        ops_doc_ids = self.opensearch_conn.get_doc_ids(source=self.user)

        # if doc in OpenSearch but not in mailbox, delete doc
        _, doc_ids_to_be_delete = not_in(ops_doc_ids, mailbox_doc_ids)

        for doc_id in doc_ids_to_be_delete:
            keyword = {"match": {"doc_id": doc_id}}
            response = self.opensearch_conn.delete_doc(keyword)

        # if doc in mailboxbut not in OpenSearch, insert doc
        mask, doc_ids_to_be_insert = not_in(mailbox_doc_ids, ops_doc_ids)
        docs_to_be_insert = [doc_content[i] for i in range(len(mask)) if not mask[i]]
        sizes_to_be_insert = [doc_sizes[i] for i in range(len(mask)) if not mask[i]]

        for i in range(len(doc_ids_to_be_insert)):
            body = self.raw_to_insert_format(doc_ids_to_be_insert[i], docs_to_be_insert[i],
                                        sizes_to_be_insert[i])
            response = self.opensearch_conn.insert_doc(body)


    def raw_to_insert_format(self, doc_id, doc_content, size):
        doc_content = email.message_from_bytes(doc_content[0][1])

        title = doc_content.get('Subject')
        gmail_url = f'https://mail.google.com/mail/u/0/#inbox/'
        send_date = doc_content.get('Date')
        sender = doc_content.get('From')
        receiver = doc_content.get('To')
        bcc = doc_content.get('BCC')
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

from sqlalchemy import create_engine, select, orm, sqlalchemy_db
from sqlalchemy.orm import sessionmaker
from model_gmail_credentials import model, GmailCredentials, Credentials
def init_db(db_name):
    
    engine = create_engine(f'sqlite:///instance/{db_name}')
    model.metadata.bind = engine
    model.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.commit()
    return DBSession

def plugin_gmail_update(plugin_instance_id):
    print("Plugin gmail update: ", plugin_instance_id)
    # get credential of plugin_instance_id

    # login
    GmailSession = Gmail(username, password)
    GmailSession.login()
    GmailSession.login_opensearch()
    GmailSession.update_email()


def plugin_gmail_init(plugin_instance_id, plugin_init_info):
    print("Plugin gmail init: ", plugin_instance_id, plugin_init_info)
    
    # create GmailCredentials table if not exist
    db_name = "PI.db"
    engine = create_engine(f'sqlite:///instance/{db_name}')
    model.metadata.bind = engine
    model.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)

    # add credentials of plugin instance
    username = plugin_init_info["username"]
    password = plugin_init_info["password"]
    plugin_instance_credentials = Credentials(plugin_instance_id, username, password)
    DBSession.add(plugin_instance_credentials)

    DBSession.commit()

# def PI_db_test(session):
#     # Use the session to interact with the database
#     requests = session.query(Request).all()
#     for row in requests:
#         print(row.id, row.request_op, row.plugin_name, row.plugin_instance_id, row.update_interval)

#     query = select(*[Request.id, Request.request_op, Request.plugin_name, Request.plugin_instance_id, Request.update_interval]).order_by(Request.id).limit(1)
#     print(query)
#     request=session.execute(query).fetchone()
#     print(request)


def plugin_gmail_del(plugin_instance_id):
    print("Plugin gmail del: ", plugin_instance_id)

    db_name = "PI.db"
    engine = create_engine(f'sqlite:///instance/{db_name}')
    DBSession = sessionmaker(bind=engine)

    # delete row with plugin_instance_id
