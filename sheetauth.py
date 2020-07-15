'''
OAuth2 authentication for personal calendar
'''

import sys
import pygsheets
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def sheetauth(directory, sheet_secret_path):
    """
    sheetauth sheetauth authentication process for google sheet
    
    Args:
        directory (string): location of where to store credential json file
        sheet_secret_path (string): path to my secret file (including name)
    """
    pygsheets.authorize(
        client_secret= sheet_secret_path,
        credentials_directory=directory,
        local=True)

if __name__=="__main__":
    sheetauth(sys.argv[1], sys.argv[2])
