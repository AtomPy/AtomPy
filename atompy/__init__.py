print 'Initializing AtomPy...'

import DownloadAPI as API
import xlrd
import pandas
import os, sys
import matplotlib.pyplot as plt
from myFileModifier import ExcelToDataframe as EDF
from myFileModifier import ExcelToSources as ETS
import webbrowser
import refs

#Global Refs class for element, ion, isotope data
Refs = refs.Refs()

#Wrapper functions
def element(Z):
    return Refs.element(Z)

def elementaw(Z):
    return Refs.elementaw(Z)

def elementryd(Z):
    return Refs.elementryd(Z)

def ion(Z, N):
    return Refs.ion(Z, N)

def ionip(Z, N):
    return Refs.ionip(Z, N)

def isotope(Z, M):
    return Refs.isotope(Z, M)

def isotopeaw(Z, M):
    return Refs.isotopeaw(Z, M)

def isotopecomp(Z, M):
    return Refs.isotopecomp(Z, M)

class IonAttribute():
    def __init__(self):
        #Title
        self.title = None
        
        #Data holds the pandas dataframe
        self.data = None
        
        #List of sources
        self.sources = {}

class Ion:
    def __init__(self, _Z, _N):
        self.Z = _Z
        self.N = _N
        self.name = 'None'
        self.levels = []
        self.avalues = []
        self.collisions = []
        self.O = []
        
    def Name(self):
        return self.name
    
    def Z(self):
        return self.Z
    
    def N(self):
        return self.N
    
    def E(self, index=0, sources=False, goto=''):
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
    
    def A(self, index=0, sources=False, goto=''):
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
        name = 'wb'
        if self.Z < 10:
            name += '0' + str(self.Z)
        else:
            name += str(self.Z)
        if self.N < 10:
            name += '0' + str(self.N)
        else:
            name += str(self.N)
        self.name = name
    
    def __str__(self):
        myString = ''
        myString += 'Ion: ' + self.Name() + ' \n'
        
        #E Sheet Count
        if len(self.levels) == 0:
            myString += '  No E sheets found...\n'
        else:
            for num in range(len(self.levels)):
                myString += '  E' + str(num) + ': ' + self.levels[num].title + '\n'
        
        #A Sheet Count
        if len(self.avalues) == 0:
            myString += '  No A sheets found...\n'
        else:
            for num in range(len(self.avalues)):
                myString += '  A' + str(num) + ': ' + self.avalues[num].title + '\n'
        
        #U Sheet Count    
        if len(self.collisions) == 0:
            myString += '  No U sheets found...\n'
        else: 
            for num in range(len(self.collisions)):
                myString += '  U' + str(num) + ': ' + self.collisions[num].title + '\n'
        
        #O Sheet Count
        if len(self.O) == 0:
            myString += '  No O sheets found...\n'
        else: 
            for num in range(len(self.O)):
                myString += '  O' + str(num) + ': ' + self.O[num].title + '\n'
                
        #Return
        return myString
    
def getE(Z1, N1, Z2 = None, N2 = None):
    
    if Z2 != None or N2 != None:
        ions = getdata(Z1, N1, Z2, N2)
        levels = {}
        for x in range(len(ions)):
            levels.append(ions[x].E())
        return levels
    else:
        return getdata(Z1, N1, Z2, N2).E()
    
def getA(Z1, N1, Z2 = None, N2 = None):
    
    if Z2 != None or N2 != None:
        ions = getdata(Z1, N1, Z2, N2)
        avalues = {}
        for x in range(len(ions)):
            avalues.append(ions[x].A())
        return avalues
    else:
        return getdata(Z1, N1, Z2, N2).A()
    
def getU(Z1, N1, Z2 = None, N2 = None):
    
    if Z2 != None and N2 != None:
        ions = getdata(Z1, N1, Z2, N2)
        collisions = {}
        for x in range(len(ions)):
            collisions.append(ions[x].U())
        return collisions
    else:
        return getdata(Z1, N1, Z2, N2).U()

def getdata(Z1, N1, Z2 = None, N2 = None):
    #Downloads various atomic data files and stores
    #them in Panda dataframes
    
    #Takes: Single data set or range of Z, N
    #Returns: Single ion or list of ions
    
    #Make sure Z and N are INTS
    Z1 = int(Z1)
    N1 = int(N1)
    
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
                NumOfO = 0
                
                for x in range(wb.nsheets):
                    if 'E' in wb.sheet_by_index(x).name:
                        NumOfE += 1
                    if 'A' in wb.sheet_by_index(x).name:
                        NumOfA += 1
                    if 'U' in wb.sheet_by_index(x).name:
                        NumOfU += 1
                    if 'O' in wb.sheet_by_index(x).name:
                        NumOfO += 1              
                
                #Extract level data
                CurrentSheet = 0
                for i in range(NumOfE):
                    levels = IonAttribute()
                    levels.title = str(wb.sheet_by_index(CurrentSheet).cell(0,0).value)
                    levels.data = EDF(wb.sheet_by_index(CurrentSheet), 
                                      ['Z','N','i-level'])
                    levels.sources = ETS(wb.sheet_by_index(CurrentSheet))
                    myIon.levels.append(levels)
                    
                    CurrentSheet += 1
                
                #Extract a value data
                for i in range(NumOfA):
                    avalues = IonAttribute()
                    avalues.title = str(wb.sheet_by_index(CurrentSheet).cell(0,0).value)
                    avalues.data = EDF(wb.sheet_by_index(CurrentSheet), 
                                       ['Z','N','j-level','i-level'])
                    avalues.sources = ETS(wb.sheet_by_index(CurrentSheet))
                    myIon.avalues.append(avalues)
                    
                    CurrentSheet += 1
                    
                #Extract collision data
                for i in range(NumOfU):
                    collisions = IonAttribute()
                    collisions.title = str(wb.sheet_by_index(CurrentSheet).cell(0,0).value)
                    collisions.data = EDF(wb.sheet_by_index(CurrentSheet), 
                                          ['Z','N','jlev','ilev','np'])
                    collisions.sources = ETS(wb.sheet_by_index(CurrentSheet))
                    myIon.collisions.append(collisions)
                   
                    CurrentSheet += 1
                    
                #Extract O data
                '''for i in range(NumOfO):
                    collisions = IonAttribute()
                    collisions.data = EDF(wb.sheet_by_index(CurrentSheet), 
                                          ['Z','N','jlev','ilev','np'])
                    collisions.sources = ETS(wb.sheet_by_index(CurrentSheet))
                    myIon.collisions.append(collisions)
                   
                    CurrentSheet += 1'''
                    
                #Generate our name
                myIon.generateName()
                
                #Set to the ion storage array
                Ions.append(myIon)
                
            #Increment loading bar
            CurrentFile = CurrentFile + 1  
            
    #Return either the single ion or the range of ions
    if len(Ions) == 1:
        print Ions[0]
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

def plot(df, xAxis, yAxis, scatter=True, line=True, color='blue'):
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
    
def plotall(df, xAxis, yAxis, fileloc=None, scatter=True, line=True, color='blue', color2='red'):
    myMarker = 'o'
    if scatter == False:
        myMarker = ' '
    
    myLine = '-'
    if line == False:
        myLine = ' '
        
    #Check to make sure the axis values are correct
    if len(xAxis) < 1:
        print 'XAxis not given...'
        return None
    if len(yAxis) < 1:
        print 'YAxis not given...'
        return None
    if len(xAxis) > len(yAxis) or len(yAxis) > len(xAxis):
        print 'Axis arrays don\'t match in length...'
        return None
        
    #Go through all of the possible indexes of the data
    for x in range(len(df.index)):
        #Create a dataframe to hold the data for this particular transition
        myDF = df
        
        #Index and build filename
        filename = ''
        for y in range(len(df.index[x])-1):
            myDF = myDF.loc[df.index[x][y]]
            filename += str(int(df.index[x][y])) + '.'
        filename = filename[:-1]
        
        #Now graph the data
        for z in range(len(xAxis)):
            plt.plot(myDF[xAxis[z]],myDF[yAxis[z]], marker=myMarker, linestyle=myLine, color=color)
            plt.plot(myDF[xAxis[z]],myDF[yAxis[z]], marker=myMarker, linestyle=myLine, color=color2)
            plt.xlabel(xAxis[z] + ' vs ' + xAxis[z])
            plt.ylabel(yAxis[z] + ' vs ' + yAxis[z])
        
        #Save the graph and close
        if(fileloc != None):
            plt.savefig(fileloc + filename + '.png')
            plt.close()
    
#Dev tools for debugging purposes
def printexpanded(df):
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
    
def printstats(df):
    #Prints some statistical data of the dataframe provided
    print df.describe()

def clear():
    os.system('cls')
    
print 'AtomPy ready!'

a = getdata(8,6)