from django.shortcuts import render
from .models import MasterRfiCatalog
from .models import MasterRfiFlaggedCatalog
from .models import CleanDev
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
from listings.choices import receiver_choices
from listings.filter_sorter import filter_sorter
from urllib.parse import urlparse,parse_qs
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

    """
    if 'Azimuth_Min' in request.GET:
        Azimuth_Min = request.GET['Azimuth_Min']
        if Azimuth_Min:
            queryset_list = MasterRfiCatalog.objects.filter(azimuth_deg_field__gt=str(Azimuth_Min)).values()
    """
    context = {
        'receiver_choices':receiver_choices,
    }

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
    return render(request,'listings/listings.html',context)
    
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
    # Pulling the url response from index.html via the ajax request in listings.html
    url = request.GET['url']
    # Parsing the url into something human-readable
    url_query = urlparse(url).query
    # Turning that url into a dictionary
    url_dict = parse_qs(url_query,keep_blank_values=False)
    # One of the url values is just from the "submit" button, so we get rid of that useless form here:
    url_dict.pop("Submit",None)
    # By default, url_dict is a list of values. But we only take one value for each question, so we're limiting this to one value per question 
    # And elimintating the list inside: 
    new_url_dict = {}
    for key,value in url_dict.items():
        if len(value) == 1:
            new_url_dict[key] = value[0]
        else: 
            raise AttributeError("Multiple values not accepted for each query type.")    
    url_dict = new_url_dict
    print(url_dict)

    # Initializing a queryset of the database table
    queryset = CleanDev.objects.all()
    # Filtering that queryset by all the values given in the url request
    filtered_queryset = filter_sorter(queryset,url_dict).getQueryset()
    filtered_queryset = filtered_queryset.values()

    
    #Create the pseudo buffer to write to so we're not storing anything large while we load the file
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    #Stream the data from the database to a file
    response = StreamingHttpResponse((writer.writerow([str(single_list['frequency_mhz']),str(single_list['intensity_jy'])]) for single_list in filtered_queryset),
                                      content_type="text/csv")
    #json_data = { "frequency":[single_list['frequency_mhz'] for single list in listings], "intensity":[single_list["intensity_jy"] for single_list in listings]}
    #Create the response as the file
    #response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    #resp = http.HttpResponse(content_type="application/json")
    #json.dump(json_data,resp)
    return response