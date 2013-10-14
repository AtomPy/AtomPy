import httplib2
import logging
logging.basicConfig()

import sys

from httplib2 import Http
from urllib import urlencode

from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

def getDriveService():
    #Gets the drive service instance using google drive credentials
    
    #Takes: nothing
    #Returns: a drive service instance
    
    try:
        #Google Drive Credentials (unique per account)
        ClientID = '230798942269.apps.googleusercontent.com'
        ClientSecret = 'JZ7dyNbQEHQ9XLXHxcFlcAad'
        OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
        REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
        
        SavedRefreshToken = '1/WjgLdc0RekqCu0s5uae1dJm9ZbmyufQWulsaXdvu3b8'
        
        h = Http()
        post_data = {'client_id':ClientID,
                     'client_secret':ClientSecret,
                     'refresh_token':SavedRefreshToken,
                     'grant_type':'refresh_token'}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        resp, content = h.request("https://accounts.google.com/o/oauth2/token", 
                                  "POST", 
                                  urlencode(post_data),
                                  headers=headers)
        content2 = content.split()
        access_token = content2[3]
        access_token = access_token.replace('"', '')
        access_token = access_token.replace(',', '')
        
        #Exchange the code / access token for credentials
        credentials = AccessTokenCredentials(access_token, ClientID)
        
        #Intialize the drive service and return it
        http = httplib2.Http()
        http = credentials.authorize(http)
        return build('drive', 'v2', http=http)
    
    #Error may occur if the user's network is down
    except httplib2.ServerNotFoundError:
        sys.exit('Can not connect to Google Drive. Please check internet connection.')
        
    #Error may occur with the server itself
    except httplib2.HttpLib2Error:
        sys.exit('Sever error. Please try again later.')
        
def getFileList(drive_service):
    #Retrieves a list of the files in the database
    
    #Takes: a drive service instance
    #Returns: a list containing the google file info
    
    #Request a list of the database files
    files = drive_service.files().list().execute()
    
    #Make sure that the files aren't in the trash or something
    onlineDataFiles = []
    for x in range(len(files['items'])):
        if files['items'][x]['labels']['hidden'] == False:
            if files['items'][x]['labels']['trashed'] == False:
                if files['items'][x]['labels']['restricted'] == False:
                    if files['items'][x]['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                        onlineDataFiles.append(files['items'][x])
    
    #Return the files
    return onlineDataFiles
