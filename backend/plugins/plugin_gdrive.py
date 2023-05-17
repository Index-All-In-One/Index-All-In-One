import asyncio, re, os, sys, datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from opensearch.conn import OpenSearch_Conn

from plugins.status_code import PluginReturnStatus
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

import json

class Gdrive_Instance:
    def __init__(self, plugin_instance_id, client_id, client_secret, access_token, refresh_token):
        self.plugin_instance_id = plugin_instance_id
        self.opensearch_conn = OpenSearch_Conn()

        self.gauth = GoogleAuth()
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        
    def login_opensearch(self, host='localhost', port=9200, username='admin', password='admin',
use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):

        try:
            self.opensearch_conn.connect(host, port, username, password,
        use_ssl, verify_certs, ssl_assert_hostname, ssl_show_warn)
            logging.debug("Opensearch login success.")
        except:
            logging.debug("Opensearch login failed.")

    def connect_gdrive(self):
        self.gauth.LoadCredentialsFile(self.creds_path)
        if self.gauth.credentials is None:
            # Authenticate the user if no credentials found
            self.gauth.LocalWebserverAuth()
            
            # Generate and save a new token
            self.gauth.SaveCredentialsFile(self.creds_path)
        else:
            # Use the saved credentials and token instead of authenticating again
            if self.gauth.access_token_expired:

                self.gauth.Refresh()
                self.gauth.SaveCredentialsFile(self.creds_path)
            else:
                try:
                    self.gauth.Authorize()
                except:
                    return False
        
        self.drive = GoogleDrive(self.gauth)
        return True
    
    def connect_drive(self, creds):
        assert(self.gauth)
        try:
            self.gauth.LoadCredentials(creds)
            self.drive = GoogleDrive(self.gauth)
        except:
            logging.debug("Error login Google Drive, invalid tokens")
            return False
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
    
    def get_token(self):
        token = {
            "access_token": self.access_token, 
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "token_uri": "https://oauth2.googleapis.com/token",
            "user_agent": None,
            "token_expiry": "2023-05-17T00:10:56Z",
            "revoke_uri": "https://oauth2.googleapis.com/revoke",
            "id_token": None,
            "id_token_jwt": None,
            "token_response": {
                "access_token": self.access_token,
                "expires_in": 3599,
                "refresh_token": self.refresh_token,
                "scope": "https://www.googleapis.com/auth/drive",
                "token_type": "Bearer"
            },
            "scopes": [
                "https://www.googleapis.com/auth/drive"
            ],
            "token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
            "invalid": False,
            "_class": "OAuth2Credentials",
            "_module": "oauth2client.client"
        }
        return json.dumps(token)




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm, Column, Integer, String

model = orm.declarative_base()
DB_NAME = "p_gdrive.db"

class GdriveCredentials(model):
    __tablename__ = 'gdrive_credentials'

    id = Column(Integer, primary_key=True)
    plugin_instance_id = Column(String(50), nullable=True)
    access_token = Column(String(100), nullable=False)
    refresh_token = Column(String(100), nullable=False)

    def __init__(self, plugin_instance_id, access_token, refresh_token):
        self.plugin_instance_id = plugin_instance_id
        self.access_token = access_token
        self.refresh_token = refresh_token


def plugin_gdrive_init(plugin_instance_id, plugin_init_info=None):

    def db_init(plugin_instance_id, access_token, refresh_token):
        # create an engine that connects to the database
        engine = create_engine(f'sqlite:///instance/{DB_NAME}')
        model.metadata.bind = engine
        model.metadata.create_all(engine)
        # create a session factory that uses the engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        # create new or update GmailCredentials object and add it to the database
        plugin_instance_credentials = session.query(GdriveCredentials).filter_by(plugin_instance_id=plugin_instance_id).first()
        if plugin_instance_credentials is None:
            plugin_instance_credentials = GdriveCredentials(plugin_instance_id, access_token, refresh_token)
        # create an engine that connects to the database
        else:
            plugin_instance_credentials.plugin_instance_id = plugin_instance_id
            plugin_instance_credentials.access_token = access_token
            plugin_instance_credentials.refresh_token = refresh_token
        
        session.commit()

    def gauth_callback():
        access_token = plugin_init_info["access_token"]
        refresh_token = plugin_init_info["refresh_token"]
        logging.info(f"access_token: {access_token}")
        logging.info(f"refresh_token: {refresh_token}")

        session = Gdrive_Instance(plugin_instance_id, access_token, refresh_token)
        status = session.connect_drive()
        if not status:
            logging.error(f'init google drive plugin instance {plugin_instance_id} failed, wrong credentials')
            return PluginReturnStatus.EXCEPTION
        
        try:
            db_init(plugin_instance_id, access_token, refresh_token)
        
        except Exception as e:
            logging.error(f'init google drive plugin instance {plugin_instance_id} failed. Incomplete client_secrets, {e}')
            return PluginReturnStatus.EXCEPTION
        
        logging.info(f'Google Drive plugin instance {plugin_instance_id} initialized, db name: {DB_NAME}')
        return PluginReturnStatus.SUCCESS

    def verify():
        # create an engine that connects to the database
        engine = create_engine(f'sqlite:///instance/{DB_NAME}')
        model.metadata.bind = engine
        model.metadata.create_all(engine)
        # create a session factory that uses the engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        # create new or update GmailCredentials object and add it to the database
        plugin_instance_credentials = session.query(GdriveCredentials).filter_by(plugin_instance_id=plugin_instance_id).first()
        if plugin_instance_credentials is None:
            logging.error(f'init google drive plugin instance {plugin_instance_id} failed, token do not exist')
            return PluginReturnStatus.EXCEPTION
        
        logging.info(f'Google Drive plugin instance {plugin_instance_id} token exists, db name: {DB_NAME}')
        return PluginReturnStatus.SUCCESS
    

    # in `/GOAuthCB`:
    # - get `auth_token` and `plugin_instance_id` .
    # - construct plugin_init_info with `auth_token`
    # - call plugin_xxx_init to store them
    if plugin_init_info:
        return gauth_callback()

    # In link new account, submit (call `add_PI`):
    # - call plugin_xxx_init with only `plugin_instance_id` to verify that we already get token.
    else:
        return verify()



def plugin_gdrive_del(plugin_instance_id):
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
    access_token = creds.access_token
    refresh_token = creds.refresh_token

    # update
    session = Gdrive_Instance(plugin_instance_id, access_token, refresh_token)
    session.connect_drive()
    session.login_opensearch(host=opensearch_hostname)
    session.update_messages()

    return PluginReturnStatus.SUCCESS

def plugin_gdrive_info_def():
    return PluginReturnStatus.SUCCESS, {
            "field_def": [\
                {
                    "field_name": "access_token", \
                    "display_name": "access_token", \
                    "type": "text_opt",
                }, \
                {
                    "field_name": "refresh_token", \
                    "display_name": "refresh_token", \
                    "type": "text_opt",
                }, \
            ],}

def test1():

    plugin_instance_id = "1"
    access_token= "ya29.a0AWY7CklNleuczWsksjwaq4dyvYPKMzdvKl-tj4oCJ_jo0NxysTdQuezNuWamZap2BLmbVDfu1U_9QBxdpqLasFqfhD5a42Q_iuZPcWYJUL1OVRlbhoIqhALYOLLSf6GtdMR4DfXAM4XHgYASSD2sYfPsQ0BDaCgYKAfYSARISFQG1tDrppGRHgcfi1YApJwEuaS5yEQ0163"
    refresh_token= "1//06MLfjX4NeBNwCgYIARAAGAYSNwF-L9Irb_lrYguaf5zI9afyraJ26G2TtWyHUeZkDmLvmg5ZaysKcn5CQlfk7Qs8B6Z3Mbd7DT8"
    client_id = "648578717595-gsinm4bqjdfogqmpbqok8ip6h109vu9v.apps.googleusercontent.com",
    client_secret = "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",

    client_secrets = {
        "installed": {
            "client_id": "648578717595-gsinm4bqjdfogqmpbqok8ip6h109vu9v.apps.googleusercontent.com",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_secret": "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",
            "redirect_uris": [
                "http://localhost"
            ]
        }
    }

    session = Gdrive_Instance(plugin_instance_id, client_id, client_secret, access_token, refresh_token)
    # session.gauth.settings = client_secrets
    token = session.get_token()
    res = session.connect_drive(token)
    print(res)
    session.login_opensearch()
    _, docs = session.get_messages()

    with open("res.txt", 'w') as f:
        f.write(str(docs))

if __name__ == "__main__":
    test1()