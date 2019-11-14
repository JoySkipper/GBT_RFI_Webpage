from django.shortcuts import render
from .models import MasterRfiCatalog
from .models import MasterRfiFlaggedCatalog
import json
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.ndimage import gaussian_filter1d
from scipy.ndimage import median_filter
from django.db.models import F
import pylab
import pandas as pd
import numpy as np
from django.db.models import Avg
from django.http import StreamingHttpResponse, HttpResponse
import csv
import time
# Create your views here.

import cProfile


from django.views.decorators.csrf import csrf_exempt


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value



def index(request):
    #max frequency value
    greatest_freq = 1373.0
    least_freq = 1372.0
    #range and steps needed if we end up doing the interactive graph. 
    #range_freqs = float(greatest_freq - float(least_freq))
    #step_value = range_freqs/20.0

    #This block is for the interactive graph. It goes through each step in frequency and averages the intensity for that frequency range, then appends it to listings
    """
    listings = []
    mysql_queries = []
    for step in np.arange(least_freq,greatest_freq,step_value):
        #mysql_queries.append("SELECT frequency_mhz,")
        listing = MasterRfiCatalog.objects.filter(frequency_mhz__gt=str(step)).filter(frequency_mhz__lt=str(step+step_value)).distinct().aggregate(Avg('intensity_jy')).values()
        freq_temp = step+step_value/2.0
        print(freq_temp)
        listings.append([freq_temp,float(list(listing)[0])])
    """

    """
    #Calls all values from the database in a given frequency range
    listings = MasterRfiCatalog.objects.filter(frequency_mhz__gt=str(least_freq)).filter(frequency_mhz__lt=str(greatest_freq)).distinct().values()
    #Create the pseudo buffer to write to so we're not storing anything large while we load the file
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    #Stream the data from the database to a file
    response = StreamingHttpResponse((writer.writerow([str(single_list['frequency_mhz']),str(single_list['intensity_jy'])]) for single_list in listings),
                                     content_type="text/csv")
    #Create the response as the file
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    #print("listings: "+str(listings))
    """
    #right now, we're not returning the downloaded file, just the static HTML page
    return render(request,'listings/listings.html')
    
    """
    context_dict = {}
    context_dict['data'] = json.dumps(listings,cls=DjangoJSONEncoder)
    return render(request, 'listings/listings.html',context_dict)
    """

def listing(request):
    return render(request, 'listings/listing.html')

def search(request):
    return render(request, 'listings/search.html')

def waiting(request):
    return render(request, 'listings/waiting.html')

def validate_username(request):
    username_data = {"is_taken":True}
    return JsonResponse(username_data)

@csrf_exempt
def django_save_me(request):
    least_freq = request.GET['least_freq']
    greatest_freq = request.GET['greatest_freq']
    #Calls all values from the database in a given frequency range ---make this the data ajax request
    listings = MasterRfiCatalog.objects.filter(frequency_mhz__gt=str(least_freq)).filter(frequency_mhz__lt=str(greatest_freq)).values()
    #check up on distinct()
    #Create the pseudo buffer to write to so we're not storing anything large while we load the file
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    #Stream the data from the database to a file
    response = StreamingHttpResponse((writer.writerow([str(single_list['frequency_mhz']),str(single_list['intensity_jy'])]) for single_list in listings),
                                      content_type="text/csv")
    #json_data = { "frequency":[single_list['frequency_mhz'] for single list in listings], "intensity":[single_list["intensity_jy"] for single_list in listings]}
    #Create the response as the file
    #response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    #resp = http.HttpResponse(content_type="application/json")
    #json.dump(json_data,resp)
    return response