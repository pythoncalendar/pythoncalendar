'''
OAuth2 authentication for personal calendar
'''

import sys
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def calauth(directory, cal_secret_path):
    """
    calauth authentication process for calendar

    Args:
        directory (string): directory to store new credential file
        cal_secret_path (string): path to my secret file (including name)
    """
    pklstr = directory + '/token.pkl'
    scopes = ['https://www.googleapis.com/auth/calendar']
    if os.path.exists(pklstr):
        with open(pklstr, "rb") as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
        cal_secret_path,
        scopes=scopes)
        credentials = flow.run_local_server(port=0)
        with open(pklstr, "wb") as token:
            pickle.dump(credentials, token)


if __name__=="__main__":
    calauth(sys.argv[1], sys.argv[2])