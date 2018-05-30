#!/usr/bin/env python

import gdcStuff as gdc
import pprint
from requests.exceptions import HTTPError

def main():
    endpoint = "projects"
    #query = {"project_id" : "TCGA-GBM"}
    filters = {
        "op" : "=", 
        "content" : {
            "field" : "project_id", 
            "value" : [ "TCGA-GBM" ]
        }
    }
    try:
       #data = gdc.runQuery(endpoint,  query,  False)
       data = gdc.runProjectQuery(endpoint,  "/TCGA-GBM?expand=summary,summary.experimental_strategies",  False)
       #data = gdc.runGetQuery(endpoint,  filters,  False)
       #data = gdc.runPostQuery(endpoint,  filters,  False)
    except HTTPError as exception:
        pprint.pprint(exception)
    except ValueError as exception:
        pprint.pprint(exception)
        
    pprint.pprint(data)

if __name__ == "__main__":
    main()
