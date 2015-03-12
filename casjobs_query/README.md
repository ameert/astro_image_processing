CasJobs Scripts
================
The casjobs\_query directory contains code for interacting with the on-line SDSS database on 
the SDSS3 website. It has a main class for queries and a few prewritten examples showing how to use or modify the class.

Description of important files
---------------------
* __casjobs\_functions.py__ -
    This holds the query\_class which is used for the queries. The class will not run as-is. THe user must, at the minimum, specify a query by writing a derived class and defining the _catalog\_query_ function that returns a properly formatted SQL query for the SDSS CasJobs webserver.
* __casjobs\_spec\_query.py__ -
    This holds a functioning code that will extract all spectroscopic galaxies from SDSS.
* __casjobs\_field\_query.py__ -
    This holds a functioning code that will extract all objects within the provided list of fields from SDSS.
* __casjobs\_ra\_dec\_search.py__ -
    This holds a functioning code that will match a provided list of galaxies with ra/dec/z coordinates and return the matches from SDSS. This is the most modified version of the query\_class. The id/ra/dec/z information is designed to come from a SQL table. However, this can be modified by the user.
* __casjobs.jar__ -
    The compiled Java program distributed by SDSS for interacting with the CasJobs service.
* __additional scripts__ - There are additional scripts in this directory that I have previously used to clean the data and load into a SQL table. These scripts are not necessary and have not been cleaned up or properly commented. However, you are free to use them.

