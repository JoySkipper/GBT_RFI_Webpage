from django.urls import path,re_path
from django.conf.urls import url

from . import views

urlpatterns = [

    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('waiting', views.waiting, name='waiting'),
    path('search', views.search, name='search'),
    path('django_save_me', views.django_save_me, name='django_save_me'),
    re_path(r'^ajax/validate_username/$',views.validate_username,name="validate_username"),

] 