#!/usr/bin/env python

import requests
import pprint
import json

def runGetQuery(endpoint,  query,  verbose):
    baseURL = "https://api.gdc.cancer.gov/"
    if query is None:
        raise ValueError("No query provided")
    if endpoint is None:
        raise ValueError("No Endpoint provided")
        
    url = baseURL + endpoint
    if isinstance(query,  dict):
        data = requests.get(url,  params = json.dumps(query))
        pprint.pprint(data.url)
        
    if data.status_code == requests.codes.ok:
        return data.json()
    else:
        data.raise_for_status()
        
def runPostQuery(endpoint,  query,  verbose):
    headers = {"Content-Type" : "application/json"}
    baseURL = "https://api.gdc.cancer.gov/"
    if query is None:
        raise ValueError("No query provided")
    if endpoint is None:
        raise ValueError("No Endpoint provided")
        
    url = baseURL + endpoint
    if isinstance(query,  dict):
        data = requests.post(url,  headers=headers,  data = json.dumps(query))
    if data.status_code == requests.codes.ok:
        return data.json()
    else:
        data.raise_for_status()
        
        
def runProjectQuery(endpoint,  query,  verbose):
    baseURL = "https://api.gdc.cancer.gov/"
    if query is None:
        raise ValueError("No query provided")
    if endpoint is None:
        raise ValueError("No Endpoint provided")
        
    url = baseURL + endpoint + query
    data = requests.get(url)
    pprint.pprint(data.url)
        
    if data.status_code == requests.codes.ok:
        return data.json()
    else:
        data.raise_for_status()
        
