

class filter_sorter: 

    def __init__(self, queryset, userOptions = {}):
        self.queryset = queryset
        
        self.OperationSetterFunctionLibrary = {
            'receiver' : self.setReceiverName,
            'filename' : self.setFilename, 
            'projid' : self.setProjid,
            'oldest_scan_date' : self.setDateMin,
            'newest_scan_date' : self.setDateMax, 
            'azimuth_min' : self.setAzimuthMin, 
            'azimuth_max' : self.setAzimuthMax, 
            'elevation_min' : self.setElevationMin, 
            'elevation_max' : self.setElevationMax,
            'frequency_min' : self.setFreqMin, 
            'frequency_max' : self.setFreqMax, 
        }

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
        #oldest_scan_date.split("_")
        #oldest_scan_year = oldest_scan_date[0]
        #oldest_scan_month = oldest_scan_date[1]
        #oldest_scan_day = oldest_scan_date[2]
        #self.queryset = self.queryset.filter(date__gt = datetime.date(oldest_scan_year,oldest_scan_month,oldest_scan_day))
        self.queryset = self.queryset.filter(date__gt = oldest_scan_date)
    def setDateMax(self, newest_scan_date):
        #newest_scan_date.split("_")
        #newest_scan_year = newest_scan_date[0]
        #newest_scan_month = newest_scan_date[1]
        #newest_scan_day = newest_scan_date[2]
        #self.queryset = self.queryset.filter(date__lt = datetime.date(newest_scan_year,newest_scan_month,newest_scan_day))
        self.queryset = self.queryset.filter(date__lt = newest_scan_date)
    def setAzimuthMin(self, azimuth_min):
        self.queryset = self.queryset.filter(azimuth_deg__gt = azimuth_min)
    def setAzimuthMax(self, azimuth_max):
        self.queryset = self.queryset.filter(azimuth_deg__lt = azimuth_max)
    def setElevationMin(self, elevation_min):
        self.queryset = self.queryset.filter(elevation_deg__gt = elevation_min)
    def setElevationMax(self, elevation_max):
        self.queryset = self.queryset.filter(elevation_deg__lt = elevation_max)
    def setFreqMin(self, frequency_min):
        self.queryset = self.queryset.filter(frequency_mhz__gt = frequency_min)
    def setFreqMax(self, frequency_max):
        self.queryset = self.queryset.filter(frequency_mhz__lt = frequency_max)

    def getQueryset(self):
        return self.queryset
        