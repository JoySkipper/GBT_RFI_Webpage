## GBT_RFI_Webpage

Contains the Django Python code used to maintain and operate the GBT RFI public-facing webpage containing access to the RFI database. 

### Note: 

This code is still in development. There is a video demo of the prototype, which displays the eventual functionality, but the code has not been released yet for general use. 

Namely, I'm still trying to figure out the best way to organize the folders, given the required structure of Django, in a way that still makes sense to those who are not very familiar with Django. 

## User Instructions:

Currently, we have one search page, which searches the whole database. The web page is currently in production to split this into a quick search page and an advanced search page, so that common searches can be streamlined. The single search page is the one in the video demo.

On the main webpage, you will eventually be able to search for a given RFI observation given your choice of receiver. If you'd like a broader range of choices, click "advanced options" in the lower right-hand corner. Then you can choose among all the options currently available. This will do a broad general search of the entire SQL database, so it will take some time.

## Video Demo: 
We have a video demo of the Webpage here: 
https://youtu.be/Fkr3nl05R9Y
