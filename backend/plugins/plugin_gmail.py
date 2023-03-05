import imaplib, email
import re, os, sys, datetime
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from opensearch.conn import OpenSearch_Conn

IMAP_URL = 'imap.gmail.com'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class Gmail_Instance:
    def __init__(self, plugin_instance_id, username, password):
        self.plugin_instance_id = plugin_instance_id
        self.user = username
        self.password = password
        self.imap = None
        self.opensearch_conn = OpenSearch_Conn()
        

    def login_opensearch(self, host='localhost', port=9200, username='admin', password='admin',
use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):

        try:
            self.opensearch_conn.connect(host, port, username, password,
        use_ssl, verify_certs, ssl_assert_hostname, ssl_show_warn)
            print("Opensearch login success.")
        except:
            print("Opensearch login failed.")

    def login_email(self):
        try:
            self.imap = imaplib.IMAP4_SSL(IMAP_URL)
            self.imap.login(self.user, self.password)
            logging.debug("Logged in as {}!".format(self.user))
            return True
        except:
            logging.debug("Email login failed.")
            return False

    def get_emails(self, mailbox="Inbox"):
        '''
            Get the universial id, content, and size of all emails in mailbox
        '''
        # select the mailbox and get the message IDs
        self.imap.select(mailbox)
        success, message_uids = self.imap.search(None, 'ALL')
        message_uids = message_uids[0].split()

        # fetch the desired attributes for each message
        doc_ids, doc_contents, doc_sizes = [], [], []
        for num in message_uids:
            # the universial id of email
            _, doc_id = self.imap.fetch(num, '(X-GM-MSGID)')
            doc_id = re.search(r'X-GM-MSGID (\d+)', doc_id[0].decode('utf-8')).group(1)
            # the content of email
            _, message = self.imap.fetch(num, '(RFC822)')
            # the size of email
            _, size = self.imap.fetch(num, '(RFC822.SIZE)')
            size = re.search(r'RFC822.SIZE (\d+)', size[0].decode('utf-8')).group(1)

            doc_ids.append(doc_id)
            doc_contents.append(message)
            doc_sizes.append(size)

        return doc_ids, doc_contents, doc_sizes

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
        _, doc_ids_to_be_delete = self.not_in(ops_doc_ids, mailbox_doc_ids)

        for doc_id in doc_ids_to_be_delete:
            response = self.opensearch_conn.delete_doc(doc_id=doc_id)

        # if doc in mailboxbut not in OpenSearch, insert doc
        mask, doc_ids_to_be_insert = self.not_in(mailbox_doc_ids, ops_doc_ids)
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

        text_content = ''
        for part in doc_content.walk():
            if part.get_content_type() == "text/plain":
                text_content = part.get_payload(decode=True).decode('utf-8')


        send_date = send_date.split(' (')[0]
        send_date = datetime.datetime.strptime(send_date, '%a, %d %b %Y %H:%M:%S %z')
        send_date = send_date.replace(tzinfo=None)
        send_date = send_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        body = {
            "doc_id": doc_id,
            "doc_name": title,
            "doc_type": 'Email',
            "link": gmail_url,
            "source": self.user,
            "created_date": send_date,
            "modified_date": send_date,
            "summary": "Sender: {}  Receiver: {}  BCC: {}".format(sender, receiver, bcc),
            "file_size": int(size),
            "plugin_instance_id": self.plugin_instance_id,
            "content": text_content
        }
        return body


    def not_in(self, list1, list2):
        ''' return items in list1 that do not exist in list2 '''
        mask = [item in list2 for item in list1]
        res = [list1[i] for i in range(len(mask)) if not mask[i]]
        return mask, res


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm, Column, Integer, String

model = orm.declarative_base()
DB_NAME = "p_gmail.db"
class GmailCredentials(model):
    __tablename__ = 'gmail_credentials'

    id = Column(Integer, primary_key=True)
    plugin_instance_id = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __init__(self, plugin_instance_id, username, password):
        self.plugin_instance_id = plugin_instance_id
        self.username = username
        self.password = password

def plugin_gmail_init(plugin_instance_id, plugin_init_info):

    # add credentials of plugin instance
    username = plugin_init_info["username"]
    password = plugin_init_info["password"]

    # check if credentials correct
    GmailSession = Gmail_Instance(plugin_instance_id, username, password)
    status = GmailSession.login_email()
    if not status:
        logging.error(f'init Gmail plugin instance {plugin_instance_id} failed, wrong credentials')
        return False

    # create an engine that connects to the database
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    model.metadata.bind = engine
    model.metadata.create_all(engine)
    # create a session factory that uses the engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # create a new GmailCredentials object and add it to the database
    plugin_instance_credentials = GmailCredentials(plugin_instance_id, username, password)
    session.add(plugin_instance_credentials)
    session.commit()

    logging.info(f'Gmail plugin instance {plugin_instance_id} initialized, db name: {DB_NAME}')
    return True


def plugin_gmail_del(plugin_instance_id):
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # delete all OpenSearch documents of this source
    creds = session.query(GmailCredentials).filter(GmailCredentials.plugin_instance_id==plugin_instance_id).first()
    username = creds.username
    password = creds.password

    GmailSession = Gmail_Instance(plugin_instance_id, username, password)
    GmailSession.login_opensearch()
    GmailSession.opensearch_conn.delete_doc(plugin_instance_id=plugin_instance_id)

    # delete the source
    creds = session.query(GmailCredentials).filter_by(plugin_instance_id=plugin_instance_id).first()
    session.delete(creds)
    session.commit()
    return None

def plugin_gmail_update(plugin_instance_id, opensearch_hostname='localhost'):
    logging.debug(f'Gmail plugin instance {plugin_instance_id} updating, db name: {DB_NAME}')
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # get credential of plugin_instance_id
    creds = session.query(GmailCredentials).filter(GmailCredentials.plugin_instance_id==plugin_instance_id).first()
    session.commit()
    # login
    username = creds.username
    password = creds.password
    GmailSession = Gmail_Instance(plugin_instance_id, username, password)
    GmailSession.login_email()
    GmailSession.login_opensearch(host=opensearch_hostname)
    GmailSession.update_email()
    return None

def plugin_gmail_info_list():
    return None, {"hint": "Please enter your app password, not Gmail's login password. If you don't have, create one first.", \
            "field_type": {"username": "text", "password": "secret", },}

if __name__ == "__main__":

    # username = "a1415217miss@gmail.com"
    # password = "password"
    # GmailSession = Gmail_Instance(plugin_instance_id, username, password)
    # GmailSession.login_email()
    # GmailSession.login_opensearch()
    # GmailSession.update_email()

    plugin_instance_id = "2b225262-8235-4c9f-9cb9-a068f72ad181"
    dic = {"username": "a1415217miss@gmail.com", "password": ""}
    plugin_gmail_init(plugin_instance_id, dic)
    plugin_gmail_update(plugin_instance_id)
    plugin_gmail_del(plugin_instance_id)
