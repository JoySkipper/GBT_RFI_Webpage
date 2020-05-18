from django.shortcuts import render
from .models import MasterRfiCatalog
from .models import MasterRfiFlaggedCatalog
from .models import Prime_Focus,Rcvr1_2,Rcvr2_3,Rcvr4_6,Rcvr8_10,Rcvr12_18,Rcvr26_40,Rcvr40_52,Rcvr68_92,RcvrArray18_26,RcvrArray75_115,RcvrMBA1_2
from .models import latest_projects
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
from listings.filter_sorter import filter_sorter,determine_queryset
from urllib.parse import urlparse,parse_qs
from django.db import connection
import zipfile
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

    context = {
        'receiver_choices':receiver_choices,
    }

    # right now, we're not returning the downloaded file, just the static HTML page.
    # It will take care of the downloaded file
    return render(request,'listings/listings.html',context)


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

    if 'latest_projid' in url_dict:
        filtered_queryset = latest_projects.objects.filter(frontend = url_dict['receiver']).values()[0]
        projid = filtered_queryset['projid']
        final_query = 'SELECT * from '+str(projid)
    else:
        # Initializing a queryset of the database table
        queryset = determine_queryset(url_dict['receiver']).getQueryset()
        # If we're not looking for latest project, then we don't need the receiver key anymore as we've
        # Already selected the queryset based on the receiver
        url_dict.pop('receiver',None)
        # Since we're also not using the latest projid flag, we can remove it
        url_dict.pop('latest_projid',None)
        # Filtering that queryset by all the values given in the url request
        filtered_queryset = filter_sorter(queryset,url_dict).getQueryset()
        filtered_rcvr_queryset = filtered_queryset.values()
        final_query = 'SELECT frequency_mhz,intensity_jy FROM Master_RFI_Catalog WHERE Frequency_MHz in '+str(tuple([float(single_list['frequency_mhz']) for single_list in filtered_rcvr_queryset]))+' AND mjd in '+str(tuple([float(single_list['mjd']) for single_list in filtered_rcvr_queryset]))
    with connection.cursor() as cursor:
        #Create the pseudo buffer to write to so we're not storing anything large while we load the file
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        cursor.execute(final_query)
        #Stream the data from the database to a file
        response = StreamingHttpResponse((writer.writerow(row) for row in cursor.fetchall()),
                                content_type="text/csv")

    return response