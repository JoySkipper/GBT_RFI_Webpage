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
    # Return the listings page
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
     # This takes a very large query to the database and requests and returns it in
     # Bite-sized chunks to as to not overload the memory
     print('in parse_query chunk')
     with connection.cursor() as cursor:
            cursor.execute(final_query)
            with open(temp_filename,'w+') as temp_file:
                temp_file.writelines('Frequency_MHz,Intensity_Jy\n')
            for row in cursor:
		# The reason we are opening the file every line (which is, of course, slower) is so
		# That we do not overload the memory by trying to maintain the whole written file to memory
                with open(temp_filename,'a+') as temp_file:
                    txt = ''
                    for column in row:
			# Write each column, comma-separated
                        txt += str(float(column))+', '
                    # Removing last ', ' of the row
                    txt = txt[:-2]
                    txt += '\n'
                    temp_file.writelines(txt)
     print('wrote chunk to '+temp_filename)
     cursor.close()
     del cursor
     # Ensures wiping of memory:
     gc.collect()

def get_final_query(semifinal_query,temp_filename,chunk_size):
    # Takes restult from receiver table and gets final query for main table
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
    # Chunk size determines max memory load. I tailored this to vanir (4 gb ram) could be raised, and thus sped up, if allocated more
    # Chunk size is basically how many lines to process at a time, so it doesn't directly correlate to gb. 
    chunk_size = 1000000
    # Get temporary file to write to, so as to not hold in memory. 
    temp_path = tempfile.gettempdir()+'/'
    # Giving it random hash at end of file so it's unique
    random.seed()
    random_temp_file_bit = random.randint(0,100000)
    temp_filename = temp_path+"temp_file_"+str(random_temp_file_bit)+".txt"
    # If the user requested the latest project
    if 'latest_projid' in url_dict:
        filtered_queryset = latest_projects.objects.filter(frontend = url_dict['receiver']).values()[0]
	# We get the latest project ID
        projid = filtered_queryset['projid']
	# Now we can pull the required parameters from that project ID table
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
	# Parsing the final query in chunks so as to not overload memory
        p = multiprocessing.Process(target=parse_query_chunk,args=(final_query,temp_filename))
        print('starting multiprocess')
        p.start()
        p.join()
        gc.collect()
        print('written to '+temp_filename)
        print('is latest')
    # If the observer did NOT want the latest project:
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
	    # Filtering query in chunks, to not overload memory
            filtered_rcvr_queryset = filtered_queryset.order_by('-id')[start_row:start_row+chunk_size].values()
            if not filtered_rcvr_queryset:
                break
            semifinal_query = 'SELECT frequency_mhz,intensity_jy FROM Master_RFI_Catalog WHERE Frequency_MHz in '+str(tuple([float(single_list['frequency_mhz']) for single_list in filtered_rcvr_queryset]))+' AND mjd in '+str(tuple([float(single_list['mjd']) for single_list in filtered_rcvr_queryset]))+' ORDER BY ID'
	    
	    
            print('have query, starting connection')
	    # We're looking at the main table first, so final query is just the same query
            final_query = semifinal_query
	    # Parse that query in chunks
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
    # If data was written to the file, we return the temp_filename with all the data
    # FileResponse already streams this back in chunks for us, hence using it over HttpResponse which would not do this. 
    if count > 1:
        response = FileResponse(open(temp_filename,'rb'))
    else:
        response = HttpResponse('<h1>Your request received no results. Please try broadening your search parameters.</h1>',status=204)
    return response
