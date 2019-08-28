from django.contrib import admin

# Register your models here.
from .models import MasterRfiCatalog
from .models import MasterRfiFlaggedCatalog

class ListingAdmin(admin.ModelAdmin):
    list_display = ('data_ID', 'filename', 'frequency_mhz', 'intensity_jy')
    list_display_links = ('data_ID','filename')
    search_fields = ('filename','frequency_mhz')

admin.site.register(MasterRfiCatalog, ListingAdmin)
admin.site.register(MasterRfiFlaggedCatalog, ListingAdmin)