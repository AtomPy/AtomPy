import DownloadAPI as API
import xlrd
import pandas
import os
import sys
import matplotlib.pyplot as plt
from myFileModifier import ExcelToDataframe as EDF
from myFileModifier import ExcelToSources as ETS
import webbrowser

class IonAttribute():
    def __init__(self):
        #Data holds the pandas dataframe
        self.data = None
        
        #List of sources
        self.sources = {}

class Ion:
    def __init__(self, _Z, _N):
        self.Z = _Z
        self.N = _N
        self.levels = []
        self.avalues = []
        self.collisions = []
        
    def Name(self):
        return self.name
    
    def Z(self):
        return self.Z
    
    def N(self):
        return self.N
    
    def E(self, index=0, sources=False, goto=False):
        if goto != '':
            sourceLine = -1
            sourceLinkLine = -1
            for x in range(len(self.levels[index].sources)):
                if goto in self.levels[index].sources[x]:
                    sourceLine = x
                    break
            for x in range(len(self.levels[index].sources)):
                if 'http' in self.levels[index].sources[x+sourceLine]:
                    sourceLinkLine = x
                    break
            if sourceLine == -1 or sourceLinkLine == -1:
                print 'Could not find source.'
                return False
            
            url = 'http' + self.levels[index].sources[sourceLinkLine].split('http')[1]
            webbrowser.open_new_tab(url)
        return None
    
        if sources:
            print ''
            for x in range(len(self.levels[index].sources)):
                print self.levels[index].sources[x]
        else:
            return self.levels[index].data
    
    def A(self, index=0, sources=False, goto=False):
        if goto != '':
            sourceLine = -1
            sourceLinkLine = -1
            for x in range(len(self.avalues[index].sources)):
                if goto in self.avalues[index].sources[x]:
                    sourceLine = x
                    break
            for x in range(len(self.avalues[index].sources)):
                if 'http' in self.avalues[index].sources[x+sourceLine]:
                    sourceLinkLine = x
                    break
            if sourceLine == -1 or sourceLinkLine == -1:
                print 'Could not find source.'
                return False
            
            url = 'http' + self.avalues[index].sources[sourceLinkLine].split('http')[1]
            webbrowser.open_new_tab(url)
        return None
    
        if sources:
            print ''
            for x in range(len(self.avalues[index].sources)):
                print self.avalues[index].sources[x]
        else:
            return self.avalues[index].data
    
    def U(self, index=0, sources=False, goto=''):
        if goto != '':
            sourceLine = -1
            sourceLinkLine = -1
            for x in range(len(self.collisions[index].sources)):
                if goto in self.collisions[index].sources[x]:
                    sourceLine = x
                    break
            for x in range(len(self.collisions[index].sources)):
                if 'http' in self.collisions[index].sources[x+sourceLine]:
                    sourceLinkLine = x
                    break
            if sourceLine == -1 or sourceLinkLine == -1:
                print 'Could not find source.'
                return False
            
            url = 'http' + self.collisions[index].sources[sourceLinkLine].split('http')[1]
            webbrowser.open_new_tab(url)
        return None
            
        if sources:
            print ''
            for x in range(len(self.collisions[index].sources)):
                print self.collisions[index].sources[x]
        else:
            return self.collisions[index].data
        
    def generateName(self):
        name = ''
        if self.Z < 10:
            name += '0' + str(self.Z)
        else:
            name += str(self.Z)
        name += '.'
        if self.N < 10:
            name += '0' + str(self.N)
        else:
            name += str(self.N)
        self.name = name
    
    def __str__(self):
        myString = ''
        myString += 'Ion: ' + self.Name() + ' \n'
        myString += '  E: ' + str(len(self.levels)) + ' \n'
        myString += '  A: ' + str(len(self.avalues)) + ' \n'
        myString += '  U: ' + str(len(self.collisions)) + ' \n'
        return myString
    
def getE(Z1, N1, Z2 = None, N2 = None):
    
    if Z2 != None and N2 != None:
        ions = getData(Z1, N1, Z2, N2)
        levels = {}
        for x in range(len(ions)):
            levels.append(ions[x].E())
        return levels
    else:
        ion = getData(Z1, N1, Z2, N2)
        return ion.E()
    
def getA(Z1, N1, Z2 = None, N2 = None):
    
    if Z2 != None and N2 != None:
        ions = getData(Z1, N1, Z2, N2)
        avalues = {}
        for x in range(len(ions)):
            avalues.append(ions[x].A())
        return avalues
    else:
        ion = getData(Z1, N1, Z2, N2)
        return ion.A()
    
def getU(Z1, N1, Z2 = None, N2 = None):
    
    if Z2 != None and N2 != None:
        ions = getData(Z1, N1, Z2, N2)
        collisions = {}
        for x in range(len(ions)):
            collisions.append(ions[x].U())
        return collisions
    else:
        ion = getData(Z1, N1, Z2, N2)
        return ion.U()

def getData(Z1, N1, Z2 = None, N2 = None):
    #Downloads various atomic data files and stores
    #them in Panda dataframes
    
    #Takes: Single data set or range of Z, N
    #Returns: Single ion or list of ions
    
    #Start the Google API Drive Service Object
    print 'Connecting to online database...'
    driveService = API.getDriveService()
    
    #Get the list of files
    files = API.getFileList(driveService)    
    
    #Z Range
    ZRange = 1
    if Z2 == None:
        Z2 = Z1
    else:
        ZRange = Z2 - Z1 + 1
    
    #N Range
    NRange = 1
    if N2 == None:
        N2 = N1
    else:
        NRange = N2 - N1 + 1
        
    #Ion storage
    Ions = []
        
    CurrentFile = 0
    #Cycle through all of the Z values
    for Z in range(ZRange):
        #Cycle through all of the N values
        for N in range(NRange):
            #Current values
            currentZ = Z1 + Z
            currentN = N1 + N
            
            #Build the filename
            filename = ''
            if currentZ < 10:
                filename += '0' + str(currentZ)
            else:
                filename += str(currentZ)
            filename += '.'
            if currentN < 10:
                filename += '0' + str(currentN)
            else:
                filename += str(currentN)
            
            #Search for the file
            foundFile = False
            fileIndex = -1
            for x in range(len(files)):
                if files[x]['title'] == filename:
                    foundFile = True
                    fileIndex = x
            
            if foundFile == False:
                print 'Error: File not found: ' + filename
            else:
                #Print status
                print 'Downloading file: ' + filename
                
                #Download the file
                file_url = files[fileIndex]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
                resp, content = driveService._http.request(file_url)   
                
                #Output status
                size = sys.getsizeof(content) / 1024
                print 'File downloaded (' + str(size) + ' kb): ' + filename
                
                #Put the excel file into a xlrd workbook
                wb = xlrd.open_workbook(file_contents=content)
                
                #Begin setting up the ion
                myIon = Ion(currentZ, currentN)
                
                #Figure out which sheets are which data
                NumOfE = 0
                NumOfA = 0
                NumOfU = 0
                
                for x in range(wb.nsheets):
                    if 'E' in wb.sheet_by_index(x).name:
                        NumOfE += 1
                    if 'A' in wb.sheet_by_index(x).name:
                        NumOfA += 1
                    if 'U' in wb.sheet_by_index(x).name:
                        NumOfU += 1              
                
                #Extract level data
                CurrentSheet = 0
                for i in range(NumOfE):
                    levels = IonAttribute()
                    levels.data = EDF(wb.sheet_by_index(CurrentSheet), 
                                      ['Z','N','ilev'])
                    levels.sources = ETS(wb.sheet_by_index(CurrentSheet))
                    myIon.levels.append(levels)
                    
                    CurrentSheet += 1
                
                #Extract a value data
                for i in range(NumOfA):
                    avalues = IonAttribute()
                    avalues.data = EDF(wb.sheet_by_index(CurrentSheet), 
                                       ['Z','N','jlev','ilev'])
                    avalues.sources = ETS(wb.sheet_by_index(CurrentSheet))
                    myIon.avalues.append(avalues)
                    
                    CurrentSheet += 1
                    
                #Extract collision data
                for i in range(NumOfU):
                    collisions = IonAttribute()
                    collisions.data = EDF(wb.sheet_by_index(CurrentSheet), 
                                          ['Z','N','jlev','ilev','np'])
                    collisions.sources = ETS(wb.sheet_by_index(CurrentSheet))
                    myIon.collisions.append(collisions)
                   
                    CurrentSheet += 1
                
                #Set to the ion storage array
                Ions.append(myIon)
                
            #Increment loading bar
            CurrentFile = CurrentFile + 1  
            
    #Return either the single ion or the range of ions
    if len(Ions) == 1:
        return Ions[0]
    if len(Ions) > 1:
        return Ions
    
def EUnit(x,unit='cm-1'):
    #Unit conversion function
    if unit == 'Ryd':
        return x/109737.31568539
    elif unit == 'eV':
        return x*1.239841930e-4
    return x

def graphData(df, xAxis, yAxis, scatter=True, line=True, color='blue'):
    #Bug fix: Custom indexing screws everything up
    df = df.reset_index()
    
    myMarker = 'o'
    if scatter == False:
        myMarker = ' '
    
    myLine = '-'
    if line == False:
        myLine = ' '
        
    #Graph data
    plt.plot(df[xAxis],df[yAxis], marker=myMarker, linestyle=myLine, color=color)
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.show()
    
def printExpanded(df):
    #Get the current settings
    before_height = pandas.get_option('display.height')
    before_max_rows = pandas.get_option('display.max_rows')
    
    #Set to the new settings to print the dataframe correctly
    pandas.set_option('display.height', len(df)+1)
    pandas.set_option('display.max_rows', len(df)+1)
    
    #Print the dataframe
    print df
    
    #Set the settings back to the previous values
    pandas.set_option('display.height', before_height)
    pandas.set_option('display.max_rows', before_max_rows)
    
def printStats(df):
    #Prints some statistical data of the dataframe provided
    print df.describe()

def clear():
    os.system('cls')
    