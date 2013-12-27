import DownloadAPI as API
import xlrd
from myFileModifier import ExcelToDataframe as EDF

class Refs():
    def __init__(self):
        #Holds reference data for elements, ions, and isotopes
        self.element_df = None
        self.ion_df = None
        self.isotope_df = None
        
        driveService = API.getDriveService()
        files = API.getFileList(driveService) 
        
        for x in range(len(files)):
            #Get the element info
            if files[x]['title'] == 'elements':
                file_url = files[x]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
                resp, content = driveService._http.request(file_url)
                wb = xlrd.open_workbook(file_contents=content)
                self.element_df = EDF(wb.sheet_by_index(0),['Z'])
                continue
            #Get the ion info
            if files[x]['title'] == 'ions':
                file_url = files[x]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
                resp, content = driveService._http.request(file_url)
                wb = xlrd.open_workbook(file_contents=content)
                self.ion_df = EDF(wb.sheet_by_index(0),['Z','N'])
                continue
            #Get the isotope info
            if files[x]['title'] == 'isotopes':
                file_url = files[x]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
                resp, content = driveService._http.request(file_url)
                wb = xlrd.open_workbook(file_contents=content)
                self.isotope_df = EDF(wb.sheet_by_index(0),['Z','M'])
                continue
        
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