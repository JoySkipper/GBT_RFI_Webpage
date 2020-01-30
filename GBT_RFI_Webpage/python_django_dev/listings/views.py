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

    return response