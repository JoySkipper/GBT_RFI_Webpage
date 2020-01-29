## GBT_RFI_Webpage

Welcome to the GBT RFI Webpage documentation. Here we cover instructions on a self-hosted webpage.  

### Note: 

This code is still in development. There is a [video demo](https://youtu.be/Fkr3nl05R9Y) of the prototype, which displays the eventual functionality, but the web page has not been released yet for general use. 


Currently, we have one search page, which searches the whole database. The web page is currently in production to split this into a quick search page and an advanced search page, so that common searches can be streamlined. The single search page is the one in the video demo.

### Planned: 

On the main webpage, you will eventually be able to search for a given RFI observation given your choice of receiver. If you'd like a broader range of choices, you will have the option to click "advanced options" in the lower right-hand corner. Then you can choose among all the options currently available. This will do a broad general search of the entire SQL database, so it will take some time.


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
* Access to either the GBO RFI database (if a GBO employee) or access to another database to which you'd like similar functionality

First you will need to clone the repository locally: 

```
git clone https://github.com/JoySkipper/GBT_RFI_Webpage
```

You'll then need to rename settings_secure.py to settings.py and fill out the information indicated in the top: the security key, allowed hosts, and database information.

At this point, you should be able to locally run the server from the python_django_dev directory: 

```
python manage.py runserver
```

If you have any issues or questions, please email jskipper@nrao.edu.



