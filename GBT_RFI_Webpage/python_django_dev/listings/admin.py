"""
Admin area for the listings app
"""

from django.contrib import admin

# Register your models here.
from .models import MasterRfiCatalog
from .models import MasterRfiFlaggedCatalog

class ListingAdmin(admin.ModelAdmin):
    list_display = ('filename', 'frequency_mhz', 'intensity_jy')
    list_display_links = ('filename',)
    search_fields = ('filename','frequency_mhz')

admin.site.register(MasterRfiCatalog, ListingAdmin)
admin.site.register(MasterRfiFlaggedCatalog, ListingAdmin)