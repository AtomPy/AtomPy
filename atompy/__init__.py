########################
# AtomPy Main Python Script for AtomPy 2.0
# Created by Josiah Lucas Boswell (www.josiahboswell.com)
#
# This is the main script for AtomPy.
########################

print 'Initializing AtomPy...'

import DownloadAPI as API
import pandas
import os, sys
import matplotlib.pyplot as plt
import refs
import xlrd
from scipy import constants

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
        self.sources = ''

class Ion:
    def __init__(self, _Z, _N):
        self.Z = _Z
        self.N = _N
        self.name = 'None'
        self.levels = []
        self.avalues = []
        self.collisions = []
        self.object = []
        
    def Name(self):
        return self.name
    
    def Z(self):
        return self.Z
    
    def N(self):
        return self.N
    
    def E(self, index=0, sources=False):
        if sources:
            print self.levels[index].sources
        else:
            return self.levels[index].data
    
    def A(self, index=0, sources=False):
        if sources:
            print self.avalues[index].sources
        else:
            return self.avalues[index].data
    
    def U(self, index=0, sources=False):
        if sources:
            print self.collisions[index].sources
        else:
            return self.collisions[index].data
        
    def O(self, index=0, sources=False):            
        if sources:
            print self.object[index].sources
        else:
            return self.object[index].data
        
    def generateName(self):
        name = ''
        if self.Z < 10:
            name += '0' + str(self.Z)
        else:
            name += str(self.Z)
        name += '_'
        if self.N < 10:
            name += '0' + str(self.N)
        else:
            name += str(self.N)
        self.name = name
    
    def __str__(self):
        myString = ''
        myString += 'Ion: Z = ' + self.name.split('_')[0] + ', N = ' + self.name.split('_')[0] + '\n'
        
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
        if len(self.object) == 0:
            myString += '  No O sheets found...\n'
        else: 
            for num in range(len(self.object)):
                myString += '  O' + str(num) + ': ' + self.object[num].title + '\n'
                
        #Return
        return myString
    
def getE(Z1, N1):
    return getdata(Z1, N1).E()
    
def getA(Z1, N1):
    return getdata(Z1, N1).A()
    
def getU(Z1, N1):
    return getdata(Z1, N1).U()

def getO(Z1, N1):
    return getdata(Z1, N1).O()
    
def listcontent():
    API.listContent()

def getdata(Z, N):
    #Downloads various atomic data files and stores
    #them in Panda dataframes
    
    #Takes: Single data set
    #Returns: Single ion
    
    #Make sure Z and N are INTS
    Z = int(Z)
    N = int(N)

    myIon = Ion(Z, N)
            
    #Generate our name
    myIon.generateName()
    
    #Build the filename
    filename = myIon.name
    
    #Get the file
    file = API.getFile(filename)
    
    #Error may have occurred, print error
    if 'ERROR' in file:
        print file
        return None
    #If no error, continue with ion appending
    else:
        for attribute in range(len(file['worksheets'])):
            newAttribute = IonAttribute()
            newAttribute.title = file['worksheets'][attribute]['title']
            newAttribute.data = file['worksheets'][attribute]['data']
            newAttribute.sources = file['worksheets'][attribute]['sources']
            
            if 'E' in file['worksheets'][attribute]['type']:
                myIon.levels.append(newAttribute)
            if 'A' in file['worksheets'][attribute]['type']:
                myIon.avalues.append(newAttribute)
            if 'U' in file['worksheets'][attribute]['type']:
                myIon.collisions.append(newAttribute)
            if 'O' in file['worksheets'][attribute]['type']:
                myIon.object.append(newAttribute)
            
    #Return the ion
    print myIon
    return myIon
    
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