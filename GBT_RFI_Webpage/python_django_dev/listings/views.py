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

# Create your views here.

import cProfile

def index(request):
    greatest_freq = 1373.0
    least_freq = 1372.0
    range_freqs = float(greatest_freq - float(least_freq))
    step_value = range_freqs/500.0
    listings = []
    mysql_queries = []
    for step in np.arange(least_freq,greatest_freq,step_value):
        #mysql_queries.append("SELECT frequency_mhz,")
        listing = MasterRfiCatalog.objects.filter(frequency_mhz__gt=str(step)).filter(frequency_mhz__lt=str(step+step_value)).distinct().aggregate(Avg('intensity_jy')).values()
        freq_temp = step+step_value/2.0
        print(freq_temp)
        listings.append([freq_temp,float(list(listing)[0])])
     
    
    #listings.frequency_mhz = gaussian_filter1d(F('frequency_mhz'),10)
    #listings.intensity_jy = gaussian_filter1d(F('intensity_jy'),10)
    #listings.save()
    #listings = MasterRfiCatalog.objects.filter(frequency_mhz='1372.54550')
    #context_dict['listings']=json.dumps(listings)
    context_dict = {}
    #context_dict['listings_json'] = []
    #for listing in listings:
    #    row = []
    #    for parameter in listing:
    #        row.append((json.dumps(parameter,cls=DjangoJSONEncoder)))
    #    context_dict['listings_json'].append(row)
    context_dict['data'] = json.dumps(listings,cls=DjangoJSONEncoder)
    #context_dict['listings_json'] = [[(json.dumps(list(parameter),cls=DjangoJSONEncoder)) for parameter in listing for listing in listings]] 
    #context = {'listings': listings}
    #listings_json = json.dumps(list(listings),cls=DjangoJSONEncoder)
    return render(request, 'listings/listings.html',context_dict)

def listing(request):
    return render(request, 'listings/listing.html')

def search(request):
    return render(request, 'listings/search.html')
