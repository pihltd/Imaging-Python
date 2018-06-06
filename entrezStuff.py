#! /usr/bin/env/ python
# Routines useful for accessing Entrez etools

import requests
import pprint

def vPrint(doit, message):
    if doit:
        pprint.pprint(message)

def runEntrezGetQuery (service,  query,  key,  verbose):
    
    #https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.chapter2_table1
    baseURL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    services = {
    "search" : "esearch.fcgi?", 
    "summary" : "esummary.fcgi?", 
    "fetch" : "efetch.fcgi?", 
    "link" : "elink.fcgi?", 
    "info" : "einfo.fcgi?", 
    "post" : "epost.fcgi?", 
    "query" : "egquery.fcgi?", 
    "spell" : "espell.fcgi?", 
    "citation" : "ecitmatch.cgi?"
    }
    databases = [
    "bioproject",
    "biosample",
    "biosystems",
    "books",
    "cdd",
    "gap",
    "dbvar",
    "epigenomics",
    "nucest",
    "gene",
    "genome",
    "gds",
    "geoprofiles",
    "nucgss",
    "homologene",
    "mesh",
    "toolkit"
    "ncbisearch",
    "nlmcatalog",
    "nuccore",
    "omia",
    "popset",
    "probe",
    "protein",
    "proteinclusters",
    "pcassay",
    "pccompound",
    "pcsubstance",
    "pubmed",
    "pmc",
    "snp",
    "sra",
    "structure",
    "taxonomy",
    "unigene",
    "unists"
    ]
    
    #make sure there is a key provided
    if key is None:
        raise ValueError('No API key provided')
        
    #make sure that a valid Entrez service is requested
    if service not in services:
        raise ValueError('Incorrect service requested')
        
    #make sure a valid database is selected, if one is used
    if query['db'] is not None:
		if query['db'] not in databases:
			raise ValueError ('Incorrect database requested')
        
    #Query has to be provided as a python dictionary
    if isinstance(query,  dict):
            if 'retmode' not in query:
                query['retmode'] = 'json'
            if 'api_key' not in query:
                query['api_key'] = key
            #All set to run the query
            results = requests.get(baseURL+services[service],  params = query)
            vPrint(verbose,  results.url)
            vPrint(verbose,  results.status_code)
            
            if results.status_code == requests.codes.ok:
				#Fetch only returns XML, not JSON so return text
                #If there was no error, return a json object if json was requested, otherwise return text
                if service == 'fetch':
					return results.text
                elif query['retmode'] == 'json':
						return results.json()
                else:
                    return results.text
            else:
                results.raise_for_status()
    else:
        raise ValueError('Query is not a python dictionary')
        
def getdbGaPDatabases(key,  verbose):
	if key is None:
		raise ValueError('No API Key provided')
	query = {}
	dblist = runEntrezGetQuery("info",  query,  key,  verbose)
	return dblist
    
def getDBFields(db,  key,  verbose):
	if key is None:
		raise ValueError('No API Key provided')
	query = {"db" : db}
	fieldlist = runEntrezGetQuery("info",  query,  key,  verbose)
	return fieldlist
	
#The following technically isn't Entrez, but close enough
def sddpQuery(query, endpoint, verbose):
	validendpoints = ['retrieve', 'locality']
	if endpoint not in validendpoints:
		raise ValueError('Incorrect endpoint requested')

	baseURL = "https://www.ncbi.nlm.nih.gov/Traces/sdl/1/"
	url = baseURL + endpoint
	
	#Query should be a python dictionary
	if isinstance(query, dict):
		data = requests.get(url,  params=query)
		if verbose:
			pprint.pprint(data.url)
			pprint.pprint(data.status_code)
			pprint.pprint(data.json())
		return data.json()
	else:
		raise ValueError('Query is not a python dictionary')
