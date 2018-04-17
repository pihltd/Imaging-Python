#!/usr/bin/env Python

import entrezStuff as estuff
import argparse
import json

api_key = "c33b6f48dd5fd9feb3dbfcdc282f29719b09"

def cidrProjectIDS(verbose):
    query = {"db" : "gap",  "term" : "(cancer[DISEASE]) AND CIDR"}
    rdata = estuff.runEntrezGetQuery("search",  query,  api_key,  verbose)
    idlist = rdata["esearchresult"]["idlist"]
    return idlist
    
def bioProjectInfo(id,  verbose):
    query = {"db" : "bioproject",  "id" : id}
    bpdata = estuff.runEntrezGetQuery("fetch",  query,  api_key,  verbose)
    estuff.vPrint(verbose,  bpdata)
    return bpdata
    
def main(args):
    #find CIDR Projects
    projectlist = cidrProjectIDS(args.verbose)
    for id in projectlist:
        print (id)
        
    if args.testmode:
        projectlist = [projectlist[0]]
    
    for id in projectlist:
        #Find the links to BioProject
        projectquery = {"dbfrom" : "gap",  "db" : "bioproject",  "id" : id}
        projectdata = estuff.runEntrezGetQuery("link",  projectquery,  api_key,  args.verbose)
        estuff.vPrint(args.verbose,  projectdata)
        
        linklist = []
        for one in projectdata['linksets']:
            for two in one['linksetdbs']:
                linklist = two['links']
        for link in linklist:
            bpinfo = bioProjectInfo(link,  args.verbose)
            estuff.vPrint(args.verbose,  bpinfo)
    
    for id in projectlist:
        #Get Linked Samples
        linkquery = {"dbfrom" : "gap",  "db" : "biosample",  "id" : id}
        linkdata = estuff.runEntrezGetQuery("link",  linkquery,  api_key,  False)
        with open("biosample.json",  "w") as outfile:
            json.dump(linkdata,  outfile)
       # estuff.vPrint(args.verbose,  linkdata)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
    parser.add_argument("-t",  "--testmode",  action = "store_true",  help = "Run in test mode")

    args = parser.parse_args()
    main(args)
