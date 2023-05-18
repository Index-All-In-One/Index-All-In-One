import asyncio, re, os, sys, datetime, json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from opensearch.conn import OpenSearch_Conn

from plugins.status_code import PluginReturnStatus
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

SECRET_DIR = "instance/drive"

class Gdrive_Instance:
    def __init__(self, plugin_instance_id):

        self.CLIENT_SECRET_PATH = os.path.join(SECRET_DIR, "client_secret_{}.json".format(plugin_instance_id))
        self.CREDS_PATH = os.path.join(SECRET_DIR, "creds_{}.json".format(plugin_instance_id))

        self.plugin_instance_id = plugin_instance_id
        self.opensearch_conn = OpenSearch_Conn()
        self.gauth = GoogleAuth(settings_file=self.CLIENT_SECRET_PATH)
        self.gauth.settings['client_config_file'] = self.CLIENT_SECRET_PATH
        self.drive = None

    def login_opensearch(self, host='localhost', port=9200, username='admin', password='admin',
use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):

        try:
            self.opensearch_conn.connect(host, port, username, password,
        use_ssl, verify_certs, ssl_assert_hostname, ssl_show_warn)
            logging.debug("Opensearch login success.")
        except:
            logging.debug("Opensearch login failed.")

    def connect_drive(self):
        self.gauth.LoadCredentialsFile(self.CREDS_PATH)
        if self.gauth.credentials is None:
            logging.debug("Invalid CredentialFile")
            return False


        # if self.gauth.credentials is None:
        #     # Authenticate the user if no credentials found
        #     self.gauth.LocalWebserverAuth()

        #     # Generate and save a new token
        #     self.gauth.SaveCredentialsFile(self.CREDS)
        else:
            # Use the saved credentials and token instead of authenticating again
            if self.gauth.access_token_expired:

                self.gauth.Refresh()
                self.gauth.SaveCredentialsFile(self.CREDS_PATH)
            else:
                try:
                    self.gauth.Authorize()
                except:
                    return False

        self.drive = GoogleDrive(self.gauth)
        return True

    def get_messages(self):
        def get_files_recursive(folder_id='root'):
            assert(self.drive is not None)
            query = "'{}' in parents and trashed=false".format(folder_id)
            file_list = self.drive.ListFile({'q': query}).GetList()

            doc_ids = []
            docs = []
            for file in file_list:

                doc_id = file['id']
                doc_name = file['title']
                doc_type = file['mimeType']
                link = file['alternateLink']

                # created_date
                created_date_dt = datetime.datetime.fromisoformat(file['createdDate'].replace('Z', '+00:00'))
                created_date = created_date_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
                # modified_date
                modified_date_dt = datetime.datetime.fromisoformat(file['modifiedDate'].replace('Z', '+00:00'))
                modified_date = modified_date_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

                file_size = 0
                summary = "Owner: {}, Last Modifying User: {}".format(file['owners'][0]['displayName'], file['lastModifyingUser']['displayName'])

                content  = ""
                if doc_type == 'text/plain':
                    content = file.GetContentString()[:100]

                if doc_type == 'application/vnd.google-apps.folder':
                    doc_ids_r, docs_r = get_files_recursive(file['id'])
                    doc_ids += doc_ids_r
                    docs += docs_r

                else:
                    file_size = file['fileSize']

                body = {
                    "doc_id": doc_id,
                    "doc_name": doc_name,
                    "doc_type": doc_type,
                    "link": link,
                    "created_date": created_date,
                    "modified_date": modified_date,
                    "summary": summary,
                    "file_size": file_size,
                    "plugin_instance_id": self.plugin_instance_id,
                    "content": content,
                }
                doc_ids.append(doc_id)
                docs.append(body)

            return doc_ids, docs

        return get_files_recursive()

    def update_messages(self):
        doc_ids, docs = self.get_messages()
        ops_doc_ids = self.opensearch_conn.get_doc_ids(plugin_instance_id=self.plugin_instance_id)
        # if doc in OpenSearch but not in source, delete doc
        _, doc_ids_to_be_delete = self.not_in(ops_doc_ids, doc_ids)
        for doc_id in doc_ids_to_be_delete:
            response = self.opensearch_conn.delete_doc(doc_id=doc_id,plugin_instance_id=self.plugin_instance_id)

        # if doc in source but not in OpenSearch, insert doc
        mask, doc_ids_to_be_insert = self.not_in(doc_ids, ops_doc_ids)

        docs = [docs[i] for i in range(len(mask)) if not mask[i]]
        for i in range(len(docs)):
            response = self.opensearch_conn.insert_doc(docs[i])


    def not_in(self, list1, list2):
        ''' return items in list1 that do not exist in list2 '''
        mask = [item in list2 for item in list1]
        res = [list1[i] for i in range(len(mask)) if not mask[i]]
        return mask, res


def generate_client_secret(plugin_instance_id, plugin_init_info):
    os.makedirs(SECRET_DIR, exist_ok=True)

    client_secret = {
        "installed": {
            "client_id": plugin_init_info["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_secret": plugin_init_info["client_secret"],
            "redirect_uris": plugin_init_info["redirect_uris"]
        }
    }
    client_secret_file = "client_secret_{}.json".format(plugin_instance_id)
    client_secret_file = os.path.join(SECRET_DIR, client_secret_file)
    with open(client_secret_file, 'w') as f:
        json.dump(client_secret, f)

def generate_creds(plugin_instance_id, plugin_init_info):
    os.makedirs(SECRET_DIR, exist_ok=True)

    client_token = {
        "access_token": plugin_init_info["access_token"],
        "client_id": plugin_init_info["client_id"],
        "client_secret": plugin_init_info["client_secret"],
        "refresh_token": plugin_init_info["refresh_token"],
        "token_expiry": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "token_uri": "https://oauth2.googleapis.com/token",
        "user_agent": None,
        "revoke_uri": "https://oauth2.googleapis.com/revoke",
        "id_token": None,
        "id_token_jwt": None,
        "scopes": [
            "https://www.googleapis.com/auth/drive"
        ],
        "token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
        "invalid": False,
        "_class": "OAuth2Credentials",
        "_module": "oauth2client.client"
    }
    token_file = "creds_{}.json".format(plugin_instance_id)
    token_file = os.path.join(SECRET_DIR, token_file)
    with open(token_file, 'w') as f:
        json.dump(client_token, f)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm, Column, Integer, String

model = orm.declarative_base()
DB_NAME = "p_gdrive.db"

class GdriveCredentials(model):
    __tablename__ = 'gdrive_credentials'

    id = Column(Integer, primary_key=True)
    plugin_instance_id = Column(String(50), nullable=True)

    def __init__(self, plugin_instance_id):
        self.plugin_instance_id = plugin_instance_id

def plugin_gdrive_init(plugin_instance_id, plugin_init_info=None):
    # create an engine that connects to the database
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    model.metadata.bind = engine
    model.metadata.create_all(engine)
    # create a session factory that uses the engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if plugin_init_info:
        generate_client_secret(plugin_instance_id, plugin_init_info)
        generate_creds(plugin_instance_id, plugin_init_info)

        DriveSession = Gdrive_Instance(plugin_instance_id)
        status = DriveSession.connect_drive()

        if not status:
            logging.error(f'Google Drive plugin instance {plugin_instance_id} init credential failed(Oauth)')
            return PluginReturnStatus.WRONG_CREDS

        # create a new DriveCredentials object and add it to the database
        plugin_instance_credentials = GdriveCredentials(plugin_instance_id)
        session.add(plugin_instance_credentials)
        session.commit()

        logging.info(f'Google Drive plugin instance {plugin_instance_id} initialized success(Oauth), db name: {DB_NAME}')
    else:
        plugin_instance_credentials= session.query(GdriveCredentials).filter_by(plugin_instance_id=plugin_instance_id).first()

        if not plugin_instance_credentials:
            logging.error(f'Google Drive plugin instance {plugin_instance_id} initialized without credentials!')
            return PluginReturnStatus.EXCEPTION

        logging.info(f'Google Drive plugin instance {plugin_instance_id} initialized success, db name: {DB_NAME}')

    return PluginReturnStatus.SUCCESS

def plugin_gdrive_del(plugin_instance_id):

    CLIENT_SECRET_PATH = os.path.join(SECRET_DIR, "client_secret_{}.json".format(plugin_instance_id))
    CREDS_PATH = os.path.join(SECRET_DIR,  "creds_{}.json".format(plugin_instance_id))

    if os.path.exists(CLIENT_SECRET_PATH):
        os.remove(CLIENT_SECRET_PATH)
        os.remove(CREDS_PATH)

    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # delete the source
    creds = session.query(GdriveCredentials).filter_by(plugin_instance_id=plugin_instance_id).first()
    session.delete(creds)
    session.commit()
    return PluginReturnStatus.SUCCESS

def plugin_gdrive_update(plugin_instance_id, opensearch_hostname='localhost'):

    logging.debug(f'Google Drive plugin instance {plugin_instance_id} updating, db name: {DB_NAME}')
    engine = create_engine(f'sqlite:///instance/{DB_NAME}')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # get credential of plugin_instance_id
    creds = session.query(GdriveCredentials).filter(GdriveCredentials.plugin_instance_id==plugin_instance_id).first()
    session.commit()

    # update
    DriveSession = Gdrive_Instance(plugin_instance_id)
    DriveSession.login_opensearch(host=opensearch_hostname)
    DriveSession.connect_drive()
    DriveSession.update_messages()

    return PluginReturnStatus.SUCCESS

def plugin_gdrive_info_def():
    return PluginReturnStatus.SUCCESS, {"hint": "Please authorize with google before submit.", \
            "field_def":[ \
                { \
                    "field_name": "gdrive_oauth", \
                    "display_name": "Google Authorization", \
                    "type": "g_oauth", \
                    "scope": "https://www.googleapis.com/auth/drive",
                }, \
            ],}
