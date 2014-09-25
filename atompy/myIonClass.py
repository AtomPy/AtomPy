#This will be my custom dataframe based off of the pandas
#dataframe, but without the scipy/numpy requirements.

class myDF:

	def __init__(self, index=None, csvString):
	
		#If specified, the data will be indexed via these vars
		#If not specified, organized by n in order received
		#Note: The indexes will need to be the same names as the
		#columns you want to be the indexes.
		self.index = None
		
		#The raw data (csvString) is going to be assumed to be
		#in standard CSV format. Columns will be comma separated,
		#rows will be separated by newline chars.
		
		#Titles of the columns in the data table
		self.columnNames = None
		
		#The rows of the data, which will be CSV formatted
		self.rows = None
		
		#Lets process the raw data now
		#First, get our column headers
		for col in csvString.split('\n')[0].split(',');
			self.columnNames.append(col)
			
		#Now get all of the row data (headers not included)
		for i in range(1, len(csvString.split('\n')):
			self.rows.append(csvString.split('\n')[i])
		
	def __str__(self):
		myString = ''
		
		#Add column titles
		for i in range(len(self.columnNames)):
			myString += self.columnNames[i] + '\t'
		
		#Begin going through the rows of the data and adding
		#the row index and row data
		for i in range(len(self.rows)):
			for col in range(len(self.rows.split(','))):
				myString += self.rows[i].split(',')[col] + '\t'
			
		#Return final display
		return myString

class myIonAttribute():
    def __init__(self):
        #Title
        self.title = None
        
        #Data holds the dataframe
        self.data = None
        
        #List of sources
        self.sources = ''
		
class myIon:
	
	def __init__(self, Z, N):
		self.name = "";
		self.Z = Z
		self.N = N
		self.levels = []
		self.avalues = []
		self.collisions = []
		self.objects = []
		self.generateName()
		
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
            print self.objects[index].sources
        else:
            return self.objects[index].data
			
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