# Making Changes

## Navigation

Under GBT_RFI_Webpage/python_django_dev/, you will see the majority of the code. 

### Pages: 

The two pages of interest are the search page and the data acquisition page. This is where the html displaying the page lives. They are located as follows: 

### Search Page:

/GBT_RFI_Webpage/python_django_dev/btre/templates/pages/index.html

### Data Acquisition Page:

/GBT_RFI_Webpage/python_django_dev/btre/templates/listings/listings.html

### Models

These are the link between the database and the html pages. These will need to be changed if anything is changed in the database (such as when a receiver is added, or a column of data is added, etc.) These are located in: 

/GBT_RFI_Webpage/python_django_dev/btre/listings/models.py

### View

The view is the python that is able to take the html request from the user, access the database, and manipulate the request to give the response (or file) that the user wants. This is in Python and located as follows: 

/GBT_RFI_Webpage/python_django_dev/btre/listings/views.py

### Other Files of Interest

The view calls several classes and functions in the following files: 

/GBT_RFI_Webpage/python_django_dev/btre/listings/filter_sorter.py

/GBT_RFI_Webpage/python_django_dev/btre/listings/choices.py


## What to do if a receiver is added to the database: 

in the following file: 

/GBT_RFI_Webpage/python_django_dev/btre/listings/choices.py

Add the receiver information to the receiver_choices dictionary. 

in the following file: 

/GBT_RFI_Webpage/python_django_dev/btre/listings/filter_sorter.py

under the class 'determine_queryset,' ad an if statement with the corresponding receiver. 

Note: I hate the nested if-else statements, too. This was added last-minute and needs to be changes to something better. 

in the following file: 

/GBT_RFI_Webpage/python_django_dev/btre/listings/models.py

You'll need to add a class for your new receiver following the format of the classes for the other receivers. 

## Overall Structure: 

From frontend to backend, this is how the communication flows: 

An observer views the index.html file, and fills out the forms to create their HTTP Request, which then navigates the user to the data acquisition page (listings.html) as well as providing listings.html with the URL for their request. Listings.html then sends that request onto views.py, a python script which manipulates the data (using choices.py and filter_sorter.py) to create a django request to the RFI database. Django knows of the structure of this database through models.py. After receiving the filtered answer to the request, views.py then streams the data to listings.html and provides the file to the user. 
