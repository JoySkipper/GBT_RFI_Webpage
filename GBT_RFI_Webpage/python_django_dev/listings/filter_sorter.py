"""
..module:: filter_sorter.py
    :synopsis: Takes in the Django queryset and user specified options, then filters and sorts
    based on that request
..moduleauthor:: JoySkipper <jskipper@nrao.edu>
Code Origin: https://github.com/JoySkipper/GBT_RFI_Webpage
"""
class noReceiver():
    pass

class filter_sorter: 

    def __init__(self, queryset, userOptions = {}):
        self.queryset = queryset
        
        self.OperationSetterFunctionLibrary = {
            'receiver' : self.setReceiverName,
            'filename' : self.setFilename, 
            'projid' : self.setProjid,
            'oldest_scan_date' : self.setDateMin,
            'newest_scan_date' : self.setDateMax, 
            'frequency_min' : self.setFreqMin, 
            'frequency_max' : self.setFreqMax, 
            'latest_projid' : self.latest_projid,
        }
        if 'receiver' not in userOptions:
            raise noReceiver
        #Set all options that were given to us: 
        for option in userOptions: 
            setterFunction = self.OperationSetterFunctionLibrary[option]
            setterFunction(userOptions[option])
    # This class assumes all the current names of the columns. If a column is added or the name changed, this will break. 
    def setReceiverName(self, receiver):
        self.queryset = self.queryset.filter(frontend = receiver)
    def setFilename(self, filename):
        self.queryset = self.queryset.filter(filename__icontains = filename)
    def setProjid(self, projid):
        self.queryset = self.queryset.filter(projid__icontains = projid)
    def setDateMin(self, oldest_scan_date):
        self.queryset = self.queryset.filter(date__gte = oldest_scan_date)
    def setDateMax(self, newest_scan_date):
        self.queryset = self.queryset.filter(date__lte = newest_scan_date)
    def setFreqMin(self, frequency_min):
        self.queryset = self.queryset.filter(frequency_mhz__gte = frequency_min)
    def setFreqMax(self, frequency_max):
        self.queryset = self.queryset.filter(frequency_mhz__lte = frequency_max)

    def getQueryset(self):
        return self.queryset
        