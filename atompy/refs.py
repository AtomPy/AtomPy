import DownloadAPI as API

class Refs():
    def __init__(self):
        #Holds reference data for elements, ions, and isotopes
        self.element_df = None
        self.ion_df = None
        self.isotope_df = None
        
        #Get the element file
        elementFile = API.getFile('elements')
        self.element_df = elementFile['worksheets'][0]['data']
        
        #Get the ions file
        ionFile = API.getFile('ions')
        self.ion_df = ionFile['worksheets'][0]['data']
        
        #Get the isotopes file
        isotopeFile = API.getFile('isotopes')
        self.isotope_df = isotopeFile['worksheets'][0]['data']        

    def element(self, Z):
        ion = self.element_df.loc[Z]
        return (ion['Element'],ion['Symbol'])
            
    def elementaw(self, Z):
        ion = self.element_df.loc[Z]
        return (float(ion['AtomicW_R1']),float(ion['Unct_R1']))
    
    def elementryd(self, Z):
        ion = self.element_df.loc[Z]
        return (float(ion['RydConst_R1']),float(ion['Unct_R1']))
    
    def ion(self, Z, N):
        ion = self.ion_df.loc[(Z,N)]
        return (ion['Ion'],ion['GroundConf'],ion['Term'],ion['J'])
            
    def ionip(self, Z, N):
        ion = self.ion_df.loc[(Z,N)]
        return (float(ion['IP_R1']),float(ion['Unct_R1']))
    
    def isotope(self, Z, M):
        ion = self.isotope_df.loc[(Z,M)]
        return ion['Isotope']
    
    def isotopeaw(self, Z, M):
        ion = self.isotope_df.loc[(Z,M)]
        return (float(ion['AtomicW_R1']),float(ion['Unct_R1']))
    
    def isotopecomp(self, Z, M):
        ion = self.isotope_df.loc[(Z,M)]
        return (float(ion['IsoComp_R1']),float(ion['Unct_R1.1']))
