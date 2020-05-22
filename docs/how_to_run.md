## GBT_RFI_Webpage

Welcome to the GBT RFI Webpage documentation. Here we cover instructions on a self-hosted webpage. 

### Functionality: 

On the main webpage, you are able to search for a given RFI observation given your choice of receiver. You can also specify date range and the project ID, or simply select 'choose latest observation.' You will always have the option to select frequency range as well. 

## Installation: 

This webpage relies heavily on Django for Python functionality. It accesses the SQL database at GBO via mySQL. We strongly recommend familiarizing yourself with Django before continuing: 

https://www.djangoproject.com/start/

### Requirements: 

* Python 3.5+ (setup.py coming soon!)
    - numpy
    - matplotlib.pyplot 
    - decimal
    - json
    - scipy 
    - pylab
    - pandas
    - django 2.2+
    - pandas
    - decimal
    - zipfile
    - miemtypes
    - gc
    - multiprocessing
    
* Access to either the GBO RFI database (if a GBO employee) or access to another database to which you'd like similar functionality

First you will need to clone the repository locally: 

```
git clone https://github.com/JoySkipper/GBT_RFI_Webpage
```

You'll then need to rename settings_secure.py to settings.py and fill out the information indicated in the top: the security key, allowed hosts, and database information. You will also need to add a my.cnf file with your personal username and password information. See the Django documentation for more details. 

At this point, you should be able to locally run the server from the python_django_dev directory: 

```
python manage.py runserver
```

If you have any issues or questions, please email jskipper@nrao.edu.



