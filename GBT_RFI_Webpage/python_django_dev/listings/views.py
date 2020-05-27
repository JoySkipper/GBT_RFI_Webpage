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
from django.http import StreamingHttpResponse, HttpResponse, FileResponse
import csv
import time
from listings.choices import receiver_choices
from listings.filter_sorter import filter_sorter,determine_queryset
from urllib.parse import urlparse,parse_qs
from django.db import connection
import zipfile
import io
from wsgiref.util import FileWrapper
import random
import tempfile
import mimetypes
import gc
import multiprocessing
import os
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

def parse_query_chunk(final_query,temp_filename):
     print('in parse_query chunk')
     with connection.cursor() as cursor:
            #writer = csv.writer(pseudo_buffer)
            cursor.execute(final_query)
            #temp_file = open(temp_filename,"a+")
            #row = cursor.fetchone()
            #line_since_last_flush = 0
            with open(temp_filename,'w+') as temp_file:
                temp_file.writelines('Frequency_MHz,Intensity_Jy\n')
            for row in cursor:
                with open(temp_filename,'a+') as temp_file:
                    txt = ''
                    for column in row:
                        txt += str(float(column))+', '
                    # Removing last column of the row
                    txt = txt[:-2]
                    txt += '\n'
                    temp_file.writelines(txt)
     print('wrote chunk to '+temp_filename)
     cursor.close()
     del cursor
     gc.collect()

def get_final_query(semifinal_query,temp_filename,chunk_size):
    with connection.cursor() as cursor:
        cursor.execute(semifinal_query)
        records = cursor.fetchall()
        frequencies = tuple([str(float(item[0])) for item in records])
        mjds = tuple([str(float(item[1])) for item in records])
    final_query = 'SELECT frequency_mhz,intensity_jy FROM Master_RFI_Catalog WHERE Frequency_MHz in '+str(frequencies)+' AND mjd in '+str(mjds)+' ORDER BY ID'
    return(final_query)


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
    print('checking if latest projid or no')
    start_row = 0
    chunk_size = 1000000
    temp_path = tempfile.gettempdir()+'/'
    random.seed()
    random_temp_file_bit = random.randint(0,100000)
    temp_filename = temp_path+"temp_file_"+str(random_temp_file_bit)+".txt"
    if 'latest_projid' in url_dict:
        filtered_queryset = latest_projects.objects.filter(frontend = url_dict['receiver']).values()[0]
        projid = filtered_queryset['projid']
        semifinal_query = 'SELECT * from '+str(projid)
        if 'frequency_min' in url_dict:
            semifinal_query += ' WHERE Frequency_MHz > '+str(url_dict['frequency_min'])
        if 'frequency_max' in url_dict:
            semifinal_query += ' WHERE Frequency_MHz < '+str(url_dict['frequency_max'])
            if 'frequency_min' in url_dict:
                old = 'WHERE'
                new = 'AND'
                occurrence = 1
                li = semifinal_query.rsplit(old,occurrence)
                semifinal_query = new.join(li)
        print(semifinal_query)
        final_query = get_final_query(semifinal_query,temp_filename,chunk_size)
        p = multiprocessing.Process(target=parse_query_chunk,args=(final_query,temp_filename))
        print('starting multiprocess')
        p.start()
        p.join()
        gc.collect()
        print('written to '+temp_filename)
        print('is latest')
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
        print('got filtered queryset')
        while True:
            filtered_rcvr_queryset = filtered_queryset.order_by('-id')[start_row:start_row+chunk_size].values()
            if not filtered_rcvr_queryset:
                break
            semifinal_query = 'SELECT frequency_mhz,intensity_jy FROM Master_RFI_Catalog WHERE Frequency_MHz in '+str(tuple([float(single_list['frequency_mhz']) for single_list in filtered_rcvr_queryset]))+' AND mjd in '+str(tuple([float(single_list['mjd']) for single_list in filtered_rcvr_queryset]))+' ORDER BY ID'
	    
	    
            print('have query, starting connection')
            #start_row = 0
            #chunk_size = 1
            #final_query = semifinal_query + ' LIMIT '+start_row+', '+chunk_size
            final_query = semifinal_query
            p = multiprocessing.Process(target=parse_query_chunk,args=(final_query,temp_filename))
            print('starting multiprocess')
            p.start()
            p.join()
            gc.collect()
            #start_row += chunk_size
            #print('finished rows '+start_row)
            start_row += chunk_size
            print('written to '+temp_filename)

    count = 0
    # Checks if data was written to the file, or if it was just the title line (ie. the database found nothing)
    try:
        with open(temp_filename,'r+') as f:
            for line in f:
                count += 1
                if count > 1:
                    break
    except FileNotFoundError:
        count = 0
    if count > 1:
        response = FileResponse(open(temp_filename,'rb'))
    else:
        response = HttpResponse('<h1>Your request received no results. Please try broadening your search parameters.</h1>',status=204)
    return response