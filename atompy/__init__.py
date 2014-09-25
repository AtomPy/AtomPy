########################
# AtomPy Main Python Script for AtomPy 2.0
# Created by Josiah Lucas Boswell (www.josiahboswell.com)
#
# This is the main script for AtomPy.
########################

print 'Initializing AtomPy...'

import os, sys
import myIonClass
import matplotlib.pyplot as plt
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
    
def getE(Z, N):
    return getdata(Z, N).E()
    
def getA(Z, N):
    return getdata(Z, N).A()
    
def getU(Z, N):
    return getdata(Z, N).U()

def getO(Z, N):
    return getdata(Z, N).O()

def getdata(Z, N):
    #Downloads various atomic data files and stores
    #them in Panda dataframes
    
    #Takes: Single data set
    #Returns: Single ion
    
    #Make sure Z and N are INTS
    Z = int(Z)
    N = int(N)

	#Create our ion structure
    myIon = myIonClass(Z, N)
    
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