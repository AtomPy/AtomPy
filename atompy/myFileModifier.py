import xlrd
import pandas
from StringIO import StringIO

def ExcelToDataframe(_ws, _index_cols):
    #Takes: XLRD worksheet and list of indexing columns
    #Returns: Indexed Pandas dataframe
    
    #Find where the data begins
    categoryLine = -1
    for row in range(_ws.nrows):
        for col in range(_ws.ncols):
            if _ws.cell(row,col).value == 'Z':
                categoryLine = row
            if categoryLine != -1: 
                break
        if categoryLine != -1: 
            break
    
    #Extract the data and place in a csv-like string
    csv_file = ''
    currentValueAbove = ''
    lastRow = []
    for blah in range(_ws.ncols):
        lastRow.append('')
    for row in range(_ws.nrows - categoryLine):
        for col in range(_ws.ncols):
            #Get the value            
            value = _ws.cell(row+categoryLine,col).value
            
            #Bug fix: remove unicode space
            if type(value) == unicode:
                value = value.replace(u'\xa0','')
                
            #Bug fix: remove any spaces in the category line
            if row == 0:
                if ' ' in value:
                    value = value.replace(' ','')
            
            #Check for removal of parentheses
            if row == 0:
                value = str(value)
                if '(' in value:
                    firstChar = -1
                    secondChar = -1
                    for x in range(len(str(value))):
                        if '(' == str(value)[x]:
                            firstChar = x
                        if ')' == str(value)[x]:
                            secondChar = x
                    value = value.replace(str(value)[firstChar:secondChar+1],'')
                
            #For category titles, add the source reference
            if row == 0:
                valueAbove = _ws.cell(row+categoryLine-1,col).value
                if valueAbove != '':
                    currentValueAbove = valueAbove
                if currentValueAbove != '':
                    value += '_' + currentValueAbove
                    
            #Unindex value
            if value == '' and col < len(_index_cols) - 1:
                value = lastRow[col]
            
            #Bug fix: remove unicode space
            if type(value) == unicode:
                value = value.replace(u'\xa0','')
                
            #Bug fix: remove any spaces in the category line
            if row == 0:
                if ' ' in value:
                    value = value.replace(' ','')
                    
            #Bug fix: comma values within the value
            value = str(value).replace(',','-')
            
            #Add value to the CSV file
            csv_file += str(value) + ','
            lastRow[col] = value
        csv_file = csv_file[:-1] + '\n'
    
    #Now put into pandas dataframe
    df = pandas.read_csv(StringIO(csv_file), index_col=_index_cols)
    #Return it
    return df

def ExcelToSources(_ws):
    #Takes: XLRD worksheet
    #Returns: List of sources
    
    #Find where the data begins
    categoryLine = -1
    for row in range(_ws.nrows):
        if _ws.cell(row,0).value == 'Z':
            categoryLine = row
            break
    
    #Now find the first line of the sources
    #We will be looking for a colon, like S1: Blah
    sourceLine = -1
    for row in range(_ws.nrows):
        if ':' in _ws.cell(row,0).value:
            sourceLine = row
            break
    
    #Now go through and get all of the sources
    column_title = ''
    descriptionAndURL = ''
    sources = {}

    for row in range(categoryLine - sourceLine + 1):
        value = _ws.cell(row + sourceLine,0).value
        descriptionAndURL += value + ' \n'
        if 'http' in value:
            sources[len(sources)] = descriptionAndURL
            descriptionAndURL = ''

    #Now return the sources
    return sources
