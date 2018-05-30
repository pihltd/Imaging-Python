#!/usr/bin/env/ python

import requests
import pprint

def runQuery(query):
    baseURL = "https://www.ncbi.nlm.nih.gov/Traces/sdl/1/retrieve"
    data = requests.get(baseURL,  params=query)
    pprint.pprint(data.url)
    pprint.pprint(data.status_code)
    return data.json()
    
def main():
    query = {"acc" :  "SRA",  "location" : "gs.us"}
    results = runQuery(query)
    pprint.pprint(results)
    
if __name__ == "__main__":
    main()
  
