#!/usr/bin/env python

import requests
import pprint
import datetime

def vPrint(doit, message):
    if doit:
        pprint.pprint(message)
        
def runQuery (tier,  resource,  queryEndpoint,  queryParams, key ,  verbose):
    #<BaseURL><Resource><QueryEndpoint>?<QueryParameters><Format> 
    
    tcia_tiers = {"test": "https://services-test.cancerimagingarchive.net/services/v3",  
    "prod": "https://services.cancerimagingarchive.net/services/v3"}
    
     #make sure there is a key provided
    if tier not in tcia_tiers:
        raise ValueError('Use either prod or test as the tier')
    if resource is None:
        raise ValueError('No resource provided')
    if queryEndpoint  is None:
        raise ValueError('No endpoing provided')
    if key is None:
        raise ValueError('No API key provided')
        
    url = tcia_tiers[tier]+resource+queryEndpoint
    
    headers = {"api_key": key}
    
    #Query has to be provided as a python dictionary
    if isinstance(queryParams,  dict):
        if 'retmode' not in queryParams:
                queryParams['retmode'] = 'json'
                
        data = requests.get(url,  headers = headers,  params = queryParams)
        vPrint(verbose,  data.url)
        vPrint(verbose,  data.status_code)
        
        if data.status_code == requests.codes.ok:
            if queryParams['retmode'] == 'json':
                    return data.json()
            else:
                return data.text
        else:
                data.raise_for_status()
    else:
        raise ValueError('Query is not a python dictionary')
        
    return data.json()
#Print a timestamped string to a log file
def printLog (filehandle, message):
	now = datetime.datetime.now()
	timestamp = "%s-%s-%s_%s:%s:%s" % (now.month, now.day, now.year, now.hour, now.minute, now.second)
	filehandle.write(("%s\t%s\n") % (timestamp, message))
