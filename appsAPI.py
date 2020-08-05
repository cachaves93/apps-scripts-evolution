from __future__ import print_function
import pickle
import os.path
import json
import csv
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/script.projects',
'https://www.googleapis.com/auth/drive.scripts','https://www.googleapis.com/auth/script.container.ui']

homolog_script_id = '1omUO0ZnTFGCNurohbBZCdI5eo7NItk4TbG6RA_dc1qmI3_9v1KoZp9w1'

def main():
    """Calls the Apps Script API.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    script_service = build('script', 'v1', credentials=creds)
    #drive_service = build('drive', 'v3', credentials=creds)

    # Call the Apps Script API
    try:

        homolog_script_request = script_service.projects().getContent(scriptId=homolog_script_id).execute()
        #response = json.loads(homolog_script_request)

        update_files = homolog_script_request.get("files")

        update_id_file = open("scriptsId.csv","r+")

        csv_reader = csv.reader(update_id_file)

        for row in csv_reader:
            if (len(row) == 2):
                if (row[1] == "Smart Leilões Code"):
                    script_id = row[0]
                    update_script_request = script_service.projects().updateContent(
                        scriptId=script_id,
                        body = {
                            "files":update_files,
                        }
                    )

                    update_script_request.execute()

    except errors.HttpError as error:
        # The API encountered a problem.
        print(error.content)


if __name__ == '__main__':
    main()