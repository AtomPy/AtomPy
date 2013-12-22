import httplib2

import sys

from httplib2 import Http
from urllib import urlencode

from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service

import pandas
from StringIO import StringIO

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
        
        h = Http(disable_ssl_certificate_validation=True)
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
        http = Http(disable_ssl_certificate_validation=True)
        http = credentials.authorize(http)
        return build('drive', 'v2', http=http)
    
    #Error may occur if the user's network is down
    except httplib2.ServerNotFoundError:
        sys.exit('Can not connect to Google Drive. Please check internet connection.')
        
    #Unexpected error may occur
    except httplib2.HttpLib2Error, e:
        sys.exit('httplib2 exception: ' + str(e))
        
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

def getGDClient():
    #Returns a Google Drive Client object that is
    #already pre-logged with valid credentials to
    #the AtomPy database
    
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    gd_client.email = "atompython@gmail.com"
    gd_client.password = "kalamazoo01"
    gd_client.ProgrammaticLogin()     
    
    return gd_client

def getList():
    #Returns a string that mimics a directory
    #view of the database
    
    #First, lets login to our drive
    GDClient = getGDClient()
    
    #Get our query feed
    q = gdata.spreadsheet.service.DocumentQuery()
    feed = GDClient.GetSpreadsheetsFeed(query=q)
    
    #Get and return the file titles
    files = []
    for x in range(len(feed.entry)):
        files.append(feed.entry[x].title.text)
    return files

def getFile(filename):
    #Gets the file data from Google Drive with
    #the queried filename, and returns a workbook
    #object containing a list that contains
    #titles, data, and sources for each worksheet
    # (these are later transferred to Ion)
    
    #First, lets login to our drive
    GDClient = getGDClient()
    
    #Create our list object
    workbook = {'title':None,
                'worksheets':[]}
    
    #Get our query feed
    q = gdata.spreadsheet.service.DocumentQuery()
    feed = GDClient.GetSpreadsheetsFeed(query=q)

    #Now to search for the file on the drive
    found = -1
    for x in range(len(feed.entry)):
        if feed.entry[x].title.text == filename:
            found = x
            workbook['title'] = feed.entry[x].title.text
            print 'Found file: ' + workbook['title']
            break
    
    #If the file is not on the drive, return error
    if found == -1:
        return 'ERROR: ' + filename + ' not found in database.'
    else:
        print 'Downloading/converting file: ' + workbook['title']
    
    #Now get the spreadsheet ID and use it to change
    #the feed from a workbook feed to a spreadsheets
    #feed
    workbook_id = feed.entry[found].id.text.rsplit('/',1)[1]
    feed = GDClient.GetWorksheetsFeed(workbook_id)
    
    #Now cycle through all of the worksheets and add the
    #data and source information to the file object
    for x in range(len(feed.entry)):
        
        #First, lets get our worksheet ID
        worksheet_id = feed.entry[x].id.text.rsplit('/',1)[1]
        
        #Second, lets create our worksheet list object
        worksheet = {'title':feed.entry[x].title.text,#plain string
                     'data':None,#data is a Pandas dataframe
                     'sources':None}#sources are in an array
        
        #Now to get the data and sources from the worksheet
        #In order to get all of the data, we need to get the
        #spreadsheet cell feed (comes in the form of list of rows)
        customQuery = gdata.spreadsheet.service.CellQuery()
        customQuery.return_empty = "true"
        cells = GDClient.GetCellsFeed(workbook_id, worksheet_id, query=customQuery)
        nCol = int(cells.col_count.text)
        nRow = int(cells.row_count.text)
        cells = cells.entry
        
        #Now cycle through all of the rows and extract the data 
        #into a 2D Array
        rawData = []
        subRawData = []
        colCounter = 0
        for y in range(len(cells)):
            if 'type="text" />' in str(cells[y]):
                subRawData.append('empty')
            else:
                subRawData.append(str(cells[y]).split("text\">")[1].split("<")[0])
            colCounter += 1
            if colCounter == nCol:
                colCounter = 0
                rawData.append(subRawData)
                subRawData =[]
                
        #Now detect which rows/columns are empty
        rowsEmpty = [True for y in range(nRow)]
        colsEmpty = [True for y in range(nCol)]
        for y in range(len(rawData)):
            for z in range(len(rawData[y])):
                if rawData[y][z] != 'empty':
                    rowsEmpty[y] = False
                    colsEmpty[z] = False
                    
        #Now remove the detected rows/columns that are empty
        delOffset = 0
        for y in range(len(rowsEmpty)):            
            #Remove empty rows
            if rowsEmpty[y] == True:
                rawData.pop(y-delOffset)
                delOffset += 1
        delOffset = 0
        for y in range(len(rawData)):
            for z in range(len(colsEmpty)):
                #Remove empty columns
                if colsEmpty[z] == True:
                    rawData[y].pop(z-delOffset)
                    delOffset += 1
            delOffset = 0
            
        #Figure out where the category line is for
        #splitting up the file into its components
        #Also fix the category line values
        #And remove units
        categoryLine = -1
        for y in range(len(rawData)):
            if rawData[y][0] == 'Z':
                categoryLine = y
                break
        lastAddition = None
        additionModified = False
        for y in range(len(rawData[categoryLine])):
            #Remove units
            if '(' in rawData[categoryLine][y] and ')' in rawData[categoryLine][y]:
                rawData[categoryLine][y] = rawData[categoryLine][y].split('(')[0]
                
            #Remove spaces
            while ' ' in rawData[categoryLine][y]:
                rawData[categoryLine][y] = rawData[categoryLine][y].replace(' ','')
            
            #Add source info
            if lastAddition == None and rawData[categoryLine-1][y] != 'empty':
                lastAddition = rawData[categoryLine-1][y]
                additionModified = True
            
            if lastAddition != None and rawData[categoryLine-1][y] != 'empty' and additionModified == False:
                lastAddition = rawData[categoryLine-1][y]
                
            if lastAddition != None:
                rawData[categoryLine][y] += '_' + lastAddition
            additionModified = False
            
        #Now to extract the sources from the file content
        rawSources = ''
        for y in range(len(rawData)):
            #Breakpoint
            if y == categoryLine - 1:
                break
            
            #Skip first line (title already collected)
            if y == 0: 
                continue
            
            #Collect the info from the first cell
            rawSources += rawData[y][0] + '\n'
        worksheet['sources'] = rawSources
            
        #Now convert all of the empty values to NULL for
        #the Pandas dataframe
        for y in range(len(rawData)):
            for z in range(len(rawData[y])):
                if rawData[y][z] == 'empty':
                    rawData[y][z] = ''
                    
                #Bug fix: data containing commas replaced with dashes
                #Otherwise the CSV file doesnt work properly
                if ',' in rawData[y][z]:
                    rawData[y][z] = rawData[y][z].replace(',','-')
        
        #Now to convert the raw data into a csv file string
        csv_string = ''
        for y in range(len(rawData)):
            #Skip until we get to the data
            if y < categoryLine:
                continue
            
            #Convert the data
            for z in range(len(rawData[y])):
                csv_string += rawData[y][z] + ','
            csv_string = csv_string[:-1] + '\n'
            
        #Setup our dataframe
        dataframe = None
        
        #Reference data
        if 'elements' in workbook['title'] and dataframe == None:
            dataframe = pandas.read_csv(StringIO(csv_string), index_col=['Z'])
        if 'ions' in workbook['title'] and dataframe == None:
            dataframe = pandas.read_csv(StringIO(csv_string), index_col=['Z','N'])
        if 'isotopes' in workbook['title'] and dataframe == None:
            dataframe = pandas.read_csv(StringIO(csv_string), index_col=['Z','M'])
        
        #Regular data
        if 'E' in worksheet['title'] and dataframe == None:
            dataframe = pandas.read_csv(StringIO(csv_string), index_col=['Z','N','i'])
        if 'A' in worksheet['title'] and dataframe == None:
            dataframe = pandas.read_csv(StringIO(csv_string), index_col=['Z','N','k','i'])
        if 'U' in worksheet['title'] and dataframe == None:
            dataframe = pandas.read_csv(StringIO(csv_string), index_col=['Z','N','k','i','np'])
        if 'O' in worksheet['title'] and dataframe == None:
            return 'ERROR: O sheets not yet supported.'
        
        #Set our dataframe to the worksheet object
        worksheet['data'] = dataframe
        
        workbook['worksheets'].append(worksheet)
    print 'Finished worbook: ' + workbook['title']
    
    return workbook
    
    
print getList()