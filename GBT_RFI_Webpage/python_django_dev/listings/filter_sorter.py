"""
..module:: filter_sorter.py
    :synopsis: Takes in the Django queryset and user specified options, then filters and sorts
    based on that request
..moduleauthor:: JoySkipper <jskipper@nrao.edu>
Code Origin: https://github.com/JoySkipper/GBT_RFI_Webpage
"""
from .models import Prime_Focus,Rcvr1_2,Rcvr2_3,Rcvr4_6,Rcvr8_10,Rcvr12_18,Rcvr26_40,Rcvr40_52,Rcvr68_92,RcvrArray18_26,RcvrArray75_115,RcvrMBA1_2
from astropy.time import Time
import django.core.exceptions

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
        try:
            self.queryset = self.queryset.filter(date__gte = oldest_scan_date)
        except django.core.exceptions.FieldError:
            oldest_scan_date = oldest_scan_date+'T00:00:00'
            oldest_scan_datetime = Time(oldest_scan_date,format='isot',scale='utc')
            mjd = oldest_scan_datetime.mjd
            self.queryset = self.queryset.filter(mjd__gte = mjd)
    def setDateMax(self, newest_scan_date):
        try:
            self.queryset = self.queryset.filter(date__kte = newest_scan_date)
        except django.core.exceptions.FieldError:
            newest_scan_date = newest_scan_date+'T00:00:00'
            newest_scan_datetime = Time(newest_scan_date,format='isot',scale='utc')
            mjd = newest_scan_datetime.mjd
            self.queryset = self.queryset.filter(mjd__lte = mjd)
    def setFreqMin(self, frequency_min):
        self.queryset = self.queryset.filter(frequency_mhz__gte = frequency_min)
    def setFreqMax(self, frequency_max):
        self.queryset = self.queryset.filter(frequency_mhz__lte = frequency_max)

    def getQueryset(self):
        return self.queryset
        
class determine_queryset:
    def __init__(self,receiver):
        if receiver == 'Prime_Focus':
            self.queryset = Prime_Focus.objects.all()
        elif receiver == 'Rcvr1_2':
            self.queryset = Rcvr1_2.objects.all()
        elif receiver == 'Rcvr2_3':
            self.queryset = Rcvr2_3.objects.all()
        elif receiver == 'Rcvr4_6':
            self.queryset = Rcvr4_6.objects.all()
        elif receiver == 'Rcvr8_10':
            self.queryset = Rcvr8_10.objects.all()
        elif receiver == 'Rcvr12_18':
            self.queryset = Rcvr12_18.objects.all()
        elif receiver == 'Rcvr26_40':
            self.queryset = Rcvr26_40.objects.all()
        elif receiver == 'Rcvr40_52':
            self.queryset = Rcvr40_52.objects.all()
        if receiver == 'Rcvr68_92':
            self.queryset = Rcvr68_92.objects.all()
        elif receiver == 'RcvrArray18_26':
            self.queryset = RcvrArray18_26.objects.all()
        elif receiver == 'RcvrArray75_115':
            self.queryset = RcvrArray75_115.objects.all()
        elif receiver == 'RcvrMBA1_2':
            self.queryset = RcvrMBA1_2.objects.all()
    def getQueryset(self):
        return self.queryset
        