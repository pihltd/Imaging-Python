#! /usr/bin/env python

import requests
import argparse
import pprint
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event, State


def getCollections(baseURL,  resource,  key,  verbose):
    collections = []
    endpoint = "/query/getCollectionValues"
    query = {"format" : "json"}
    collection_data = runQuery(baseURL,  resource,  endpoint,  query,  key,  verbose)
    for data in collection_data:
        collections.append(data['Collection'])
    return collections
    
def runQuery (baseURL,  resource,  queryEndpoint,  queryParams, key ,  verbose):
    #<BaseURL><Resource><QueryEndpoint>?<QueryParameters><Format> 
    url = baseURL+resource+queryEndpoint
    headers = {"api_key":key}

    data = requests.get(url,  headers = headers,  params = queryParams)
    vPrint(verbose,  data.url)
    vPrint(verbose,  data.status_code)
    return data.json()

def vPrint(doit, message):
    if doit:
        pprint.pprint(message)
        
#Main application section
tcia_tiers = {"test": "https://services-test.cancerimagingarchive.net/services/v3",  "prod": "https://services.cancerimagingarchive.net/services/v3"}
resource = "/TCIA"
key = "15cda45b-397d-4439-8a37-cdb4d8e5e4ab"
tier = tcia_tiers["prod"]

collections = getCollections(tier, resource,  key,  False)
#for collection in collections:
#    print(collection)
app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.H3("Cohort"), 
        dcc.Dropdown(id='cohort_dropdown',  options = [{'label' : collection,  'value' : collection} for collection in collections])
    ]), 
    html.Div([
        html.H3("Modalities"), 
        dcc.Checklist(id='mode_checklist')
    ])
])
@app.callback(
    dash.dependencies.Output('mode_checklist',  'options'), 
    [dash.delpendencies.Input('cohort_dropdown',  'value')]
)
def getModalities(cohort):
    query = {"Collection" : cohort,  "format" : "json"}
    endpoint = "/query/getModalityValues"
    data = runQuery(tier,  resource,  endpoint, query,  key,  False )
    options = []
    for item in data:
        options.append({"label" : item,  "value" : item})
    return options
    #collection = "TCGA-GBM"
    #modequery = {"Collection" : collection,  "format" :  "json"}
    #endpoint = "/query/getModalityValues"
    #data = runQuery(tcia_tiers[args.tier],  resource,  endpoint,  modequery,  key,  args.verbose)
    #pprint.pprint(data)
    
if __name__ == "__main__":
    app.run_server(debug=True)
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
    #parser.add_argument("-t",  "--tier",  choices=["test", "prod"],  help = "API tier, test or prod")
    
    #args = parser.parse_args()
    
    #main(args)
