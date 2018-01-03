#! /usr/bin/env/ python
# Routines useful for accessing Entrez etools

import requests
import pprint

def vPrint(doit, message):
    if doit:
        pprint.pprint(message)

def runEntrezGetQuery (service,  query,  key,  verbose):
    baseURL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    services = {
    "search" : "esearch.fcgi?", 
    "summary" : "esummary.fcgi?", 
    "fetch" : "efetch.fcgi?", 
    "link" : "elink.fcgi?"
    }
    
    #make sure there is a key provided
    if key is None:
        raise ValueError('No API key provided')
        
    #make sure that a valid Entrez service is requested
    if service not in services:
        raise ValueError('Incorrect service requested')
        
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
                #If there was no error, return a json object if json was requested, otherwise return text
                if query['retmode'] == 'json':
                    return results.json()
                else:
                    return results.text
            else:
                results.raise_for_status()
    else:
        raise ValueError('Query is not a python dictionary')