#! /usr/bin/env python

import tciaStuff as tcia
import gdcStuff as gdc
from requests.exceptions import HTTPError
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event, State
import plotly.graph_objs as go
import pprint


def getCollections(tier,  resource,  key,  verbose):
    collections = []
    endpoint = "/query/getCollectionValues"
    query = {"format" : "json"}
    collection_data = tcia.runQuery(tier, resource,  endpoint,  query,  key,  verbose)
    for data in collection_data:
        collections.append(data['Collection'])
    return collections
    
def parseData(data,  key):
    counter = {}
    for item in data:
        if key in item:
            if item[key] in counter:
                counter[item[key]] = counter[item[key]] + 1
            else:
                counter[item[key]] = 1
                
    return counter
#####################################      
#                      Main application section                            #
#####################################

resource = "/TCIA"
key = "15cda45b-397d-4439-8a37-cdb4d8e5e4ab"

try:
    collections = getCollections("prod", resource,  key,  False)
except HTTPError as exception:
    pprint.pprint(exception)
except ValueError as exception:
    pprint.pprint(exception)
app = dash.Dash()
#https://codepen.io/chriddyp/pen/bWLwgP
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3("Cohort"), 
            dcc.Dropdown(id='cohort_dropdown',  options = [{'label' : collection,  'value' : collection} for collection in collections])
        ],  className = "three columns"), 
        html.Div([
            html.H3("Update"), 
            html.Button(['Update Graphs'], 
            id = 'updatebutton')
        ],  className = 'one column')
    ], className = 'row'), 
    html.Div([
        html.Div([
            html.H3("Gender"),
            dcc.Graph(id='gender_graph')
        ],  className = 'six columns'), 
        html.Div([
            html.H3("Modalities"), 
            dcc.Graph(id = 'modality_graph')
        ],  className = 'six columns')
    ],  className = 'row'), 
    html.Div([
        html.Div([
            html.H3("Body Parts"), 
            dcc.Graph(id = "body_graph")
        ],  className = 'six columns'), 
        html.Div([
            html.H3("Protocols"), 
            dcc.Graph(id = "series_graph")
        ],  className = 'six columns')
    ],  className = 'row') , 
    html.Div([
        html.Div([
            html.H3("TCGA Data"), 
            dcc.Graph(id= "tcga_graph")
        ],  className = 'six columns')
    ],  className = 'row')
])

@app.callback(
    Output('gender_graph', 'figure'), 
    state = [State('cohort_dropdown',  'value')], 
    events = [Event('updatebutton',  'click')]
)
def updateGenderGraph(selected_cohort):
    query = {"Collection" : selected_cohort}
    try:
        patients = tcia.runQuery("prod",  resource,  '/query/getPatient', query,  key,  False )
    except HTTPError as exception:
        pprint.pprint(exception)
    except ValueError as exception:
        pprint.pprint(exception)
    pprint.pprint(patients)  
    counter = parseData(patients,  'PatientSex')
    figure = {'data' : [go.Pie(labels=list(counter.keys()),  values=list(counter.values()))], 
                    'layout' : {'title' : selected_cohort}}
    return figure
    
@app.callback(
    Output('modality_graph', 'figure'), 
    state = [State('cohort_dropdown',  'value')], 
    events = [Event('updatebutton',  'click')]
)
def updateModalityGraph(selected_cohort):
    counter = {}
    query = {"Collection" : selected_cohort}
    try:
        modalities = tcia.runQuery("prod", resource,  '/query/getModalityValues',  query,  key,  False)
    except HTTPError as exception:
        pprint.pprint(exception)
    except ValueError as exception:
        pprint.pprint(exception)
    pprint.pprint(modalities)
    counter = parseData(modalities,  'Modality')
    figure = {'data' : [go.Pie(labels = list(counter.keys()),  values = list(counter.values()))], 
                    'layout' : {'title' : selected_cohort}}
    return figure

@app.callback(
    Output('body_graph', 'figure'), 
    state = [State('cohort_dropdown',  'value')], 
    events = [Event('updatebutton',  'click')]
)
def updatBodyGraph(selected_cohort):
    counter = {}
    query = {"Collection" : selected_cohort}
    try:
        parts = tcia.runQuery("prod", resource,  '/query/getBodyPartValues',  query,  key,  False)
    except HTTPError as exception:
        pprint.pprint(exception)
    except ValueError as exception:
        pprint.pprint(exception)
    pprint.pprint(parts)
    counter = parseData(parts,  'BodyPartExamined')
    figure = {'data' : [go.Pie(labels = list(counter.keys()),  values = list(counter.values()))], 
                    'layout' : {'title' : selected_cohort}}
    return figure
    
@app.callback(
    Output('series_graph', 'figure'), 
    state = [State('cohort_dropdown',  'value')], 
    events = [Event('updatebutton',  'click')]
)   
def updateSeriesGraph(selected_cohort):
    counter = {}
    query = {"Collection" : selected_cohort}
    try:
        series = tcia.runQuery("prod", resource,  '/query/getSeries',  query,  key,  False)
    except HTTPError as exception:
        pprint.pprint(exception)
    except ValueError as exception:
        pprint.pprint(exception)
    counter = parseData(series,  'ProtocolName')
    figure = {'data' : [go.Pie(labels = list(counter.keys()),  values = list(counter.values()))], 
                    'layout' : {'title' : selected_cohort}}
    return figure

@app.callback(
    Output('tcga_graph', 'figure'), 
    state = [State('cohort_dropdown',  'value')], 
    events = [Event('updatebutton',  'click')]
) 
def updateTCGAGraph(selected_cohort):
    if "TCGA" in selected_cohort:
        counter = {}
        query = ("/%s?expand=summary,summary.experimental_strategies") % (selected_cohort)
        try:
            data = gdc.runProjectQuery("projects",  query,  False)
        except HTTPError as exception:
            pprint.pprint(exception)
        except ValueError as exception:
            pprint.pprint(exception)
    strategies = data['data']['summary']['experimental_strategies']
    for strategy in strategies:
        counter[strategy['experimental_strategy']] = strategy['case_count']
        
    figure = {'data' : [go.Pie(labels = list(counter.keys()),  values = list(counter.values()))], 
                    'layout' : {'title' : selected_cohort}}
    return figure
    

if __name__ == "__main__":
    app.run_server(debug=True)
