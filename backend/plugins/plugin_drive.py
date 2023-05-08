from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Set the path to your credentials directory
creds_dir = "instance/"

# Load the client credentials file from the specified directory
secrets_path = os.path.join(creds_dir, "client_secrets.json")
gauth = GoogleAuth(settings_file=secrets_path)
gauth.settings['client_config_file'] = secrets_path

# Load the user credentials file from the specified directory
creds_path = os.path.join(creds_dir, "drive_creds.txt")
gauth.LoadCredentialsFile(creds_path)

if gauth.credentials is None:
    # Authenticate the user if no credentials found
    gauth.LocalWebserverAuth()
    
    # Generate and save a new token
    gauth.SaveCredentialsFile(creds_path)
else:
    # Use the saved credentials and token instead of authenticating again
    gauth.Authorize()

# Create a Google Drive API client
drive = GoogleDrive(gauth)


# Define a function to list files recursively
def list_files_recursive(folder_id, indent=""):
    # Get all files and directories in the specified folder
    query = "'{}' in parents and trashed=false".format(folder_id)
    file_list = drive.ListFile({'q': query}).GetList()

    # Process each file or directory in the folder
    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            # If this is a directory, print its name and list its contents
            print("{}{}/".format(indent, file['title']))
            list_files_recursive(file['id'], indent + "    ")
        else:
            # If this is a file, print its name
            print("{}{}".format(indent, file['title']))

# Retrieve and print the contents of the root directory recursively
list_files_recursive('root')

