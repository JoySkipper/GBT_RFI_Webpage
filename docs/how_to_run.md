## GBT_RFI_Webpage

Contains the Django Python code used to maintain and operate the GBT RFI public-facing webpage containing access to the RFI database. 

### Note: 

This code is still in development. There is a video demo of the prototype, which displays the eventual functionality, but the code has not been released yet for general use. 

## User Instructions:

Currently, we have one search page, which searches the whole database. The web page is currently in production to split this into a quick search page and an advanced search page, so that common searches can be streamlined. The single search page is the one in the video demo.

On the main webpage, you will eventually be able to search for a given RFI observation given your choice of receiver. If you'd like a broader range of choices, click "advanced options" in the lower right-hand corner. Then you can choose among all the options currently available. This will do a broad general search of the entire SQL database, so it will take some time.

## Developer Instructions: 

This webpage relies heavily on Django for Python functionality. It accesses the SQL database at GBO via mySQL. The search page is under GBT_RFI_Webpage/python_django_dev/templates/pages/index.html. The page displaying the search results is under GBT_RFI_Webpage/python_django_dev/templates/listings/listings.html. The advanced options page has not yet been created. This page will be updated when it is made. 