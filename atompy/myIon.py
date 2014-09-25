#This will be my custom dataframe based off of the pandas
#dataframe, but without the scipy/numpy requirements.

class myIon:
	
	def __init__(self, Z, N):
		self.name = "";
		self.Z = Z
		self.N = N
		
class myDF:

	def __init__(self):
		self.index = None
		