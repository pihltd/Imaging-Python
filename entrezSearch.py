#!/usr/bin/env Python

import requests
import requests.exceptions.HTTPError as HTTPError
import json
import argparse
import pprint



def runQuery(url,  query, verbose):
    api_key = "c33b6f48dd5fd9feb3dbfcdc282f29719b09"
    if 'api_key' not in query:
        query['api_key'] = api_key

    if 'retmode' not in query:
        query['retmode'] = 'json'
    try:
        result = requests.get(url, params=query)
        vPrint(verbose,result.url)
    except HTTPError as exception:
        pprint.pprint(exception)

    if query['retmode'] == 'json':
        return result.json()
    else:
        return result.text

def vPrint(doit, message):
    if doit:
        pprint.pprint(message)

def main(args):
        # http://www.ncbi.nlm.nih.gov/sites/entrez?cmd=search&db=gap&term=1[s_discriminator]%20AND%20(CIDR)&report=SStudies

        searchurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
        summaryurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
        fetchurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"

        query = {"db" : "gap", "term" : "1[s_discriminator] AND CIDR"}
        rdata = runQuery(searchurl,  query, args.verbose)
        vPrint(args.verbose,  rdata)

        idlist = rdata["esearchresult"]["idlist"]

        #querystring = ",".join(idlist)
        querystring = idlist[0]
        idquery = {"db" : "gap", "id" : querystring}

        if args.summary:
            summary = runQuery(summaryurl,  idquery,  args.verbose)
            f = open("summary.txt","w")
            f.write(json.dumps(summary))
            f.close()
            vPrint(args.verbose, summary)

        if args.fetch:
            idquery['retmode'] = 'text'
            fetch = runQuery (fetchurl,  idquery,  args.verbose)
            f = open("fetch.txt", "w")
            f.write(json.dumps(fetch))
            f.close()
            vPrint(args.verbose, fetch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
    parser.add_argument("-s",  "--summary",  action = "store_true",  help = "Return Summary from search")
    parser.add_argument("-f",  "--fetch",  action = "store_true",  help ="Return full document")

    args = parser.parse_args()
    main(args)
