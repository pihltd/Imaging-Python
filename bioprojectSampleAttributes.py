#!/usr/bin/env python
#TDP version of Ian's script

import entrezStuff as entrez
from requests.exceptions import HTTPError
import argparse
import pprint
import sys
#import xmltodict

def main (args):
    query = {"id" : args.bioproject, "dbfrom" : "bioproject",  "db" : "biosample",  "linkname" : "bioproject_biosample"}
    try:
        results = entrez.runEntrezGetQuery("link",  query,  args.apikey,  args.verbose)
    except ValueError as exception:
        pprint.pprint(exception)
        sys.exit()
    except HTTPError as exception:
        pprint.pprint(exception)
        
    entrez.vPrint(args.verbose,  results)
    linkcount = results['linksets'][0]['linksetdbs'][0]['links']
    print(len(linkcount))
    
    #This creates a server list
    query = {"id" : args.bioproject, "cmd" : "neighbor_history",  "dbfrom" : "bioproject",  "db" : "biosample",  "linkname" : "bioproject_biosample"}
    try:
        histres = entrez.runEntrezGetQuery("link",  query,  args.apikey,  args.verbose)
    
    except ValueError as exception:
        pprint.pprint(exception)
        sys.exit
    except HTTPError as exception:
        pprint.pprint(exception)
        
    entrez.vPrint(args.verbose,  histres)
    webenv = histres['linksets'][0]['webenv']
    querykey = histres['linksets'][0]['linksetdbhistories'][0]['querykey']
    query = {"query_key" : querykey,  "WebEnv" :  webenv,  "db" : "biosample",  "retmode" : "xml"}
    
    try:
        newres = entrez.runEntrezGetQuery("fetch",  query,  args.apikey,  args.verbose)
       # jsonnewres = xmltodict.parse(newres)
        entrez.vPrint(args.verbose,  newres)
    except ValueError as exception:
        pprint.pprint(exception)
        sys.exit
    except HTTPError as exception:
        pprint.pprint(exception)
    
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
    parser.add_argument("-k",  "--apikey",  required = True,  help = "Entrez API key")
    parser.add_argument("-b",  "--bioproject",  required = True,  help = "Bioproject ID")

    args = parser.parse_args()
    main(args)
