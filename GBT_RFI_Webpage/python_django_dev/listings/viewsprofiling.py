from django.shortcuts import render
from models import MasterRfiCatalog
from models import MasterRfiFlaggedCatalog
from decimal import Decimal
from django.db.models import Avg
from django.db import models

greatest_freq = 1373.0
least_freq = 1372.0
range_freqs = float(greatest_freq - float(least_freq))
step_value = range_freqs/5.0
listings = []
for step in np.arange(least_freq,greatest_freq,step_value):
    listing = MasterRfiCatalog.objects.filter(frequency_mhz__gt=str(step)).filter(frequency_mhz__lt=str(step+step_value)).distinct().aggregate(Avg('intensity_jy')).values()
    freq_temp = step+step_value/2.0
    print(freq_temp)
    listings.append([freq_temp,float(list(listing)[0])])
