#! /usr/bin/env/ python
# Routines useful for accessing Entrez etools

import requests
import pprint
import xml.etree.ElementTree as et

def vPrint(doit, message):
  if doit:
    pprint.pprint(message)

def runEntrezQuery (service,  query,  key, querytype,  verbose):
  #https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.chapter2_table1
  baseURL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
  services = {
  "search" : "esearch.fcgi",
  "summary" : "esummary.fcgi",
  "fetch" : "efetch.fcgi",
  "link" : "elink.fcgi",
  "info" : "einfo.fcgi",
  "post" : "epost.fcgi",
  "query" : "egquery.fcgi",
  "spell" : "espell.fcgi",
  "citation" : "ecitmatch.cgi"
  }
  databases = [
  "bioproject",
  "biosample",
  "biosystems",
  "books",
  "cdd",
  "gap",
  "dbvar",
  "epigenomics",
  "nucest",
  "gene",
  "genome",
  "gds",
  "geoprofiles",
  "nucgss",
  "homologene",
  "mesh",
  "toolkit"
  "ncbisearch",
  "nlmcatalog",
  "nuccore",
  "omia",
  "popset",
  "probe",
  "protein",
  "proteinclusters",
  "pcassay",
  "pccompound",
  "pcsubstance",
  "pubmed",
  "pmc",
  "snp",
  "sra",
  "structure",
  "taxonomy",
  "unigene",
  "unists"
  ]

  #Quertytypes allowed
  querytypes = ["get", "post"]
  if querytype not in querytypes:
    raise ValueError('Querytype must be either "get" or "post"')

  #make sure there is a key provided
  if key is None:
    raise ValueError('No API key provided')

  #make sure that a valid Entrez service is requested
  if service not in services:
    raise ValueError('Incorrect service requested')

  #make sure a valid database is selected, if one is used
  if query['db'] is not None:
    if query['db'] not in databases:
      raise ValueError ('Incorrect database requested')

  #Query has to be provided as a python dictionary
  if isinstance(query,  dict):
    if 'retmode' not in query:
      query['retmode'] = 'json'
    if 'api_key' not in query:
      query['api_key'] = key
    #All set to run the query
    if querytype == "get":
      results = requests.get(baseURL+services[service]+"?",  params = query)
    elif querytype == "post":
      results = requests.post(baseURL+services[service], data = query)
    else:
      raise ValueError('Bad Query type')
    vPrint(verbose,  results.url)
    vPrint(verbose,  results.status_code)

    if results.status_code == requests.codes.ok:
    #Fetch only returns XML, not JSON so return text
    #If there was no error, return a json object if json was requested, otherwise return text
      if service == 'fetch':
        return results.text
      elif query['retmode'] == 'json':
        return results.json()
      else:
        return results.text
    else:
      results.raise_for_status()
  else:
    raise ValueError('Query is not a python dictionary')

def getdbGaPDatabases(key,  verbose):
	if key is None:
		raise ValueError('No API Key provided')
	query = {}
	dblist = runEntrezGetQuery("info",  query,  key,  verbose)
	return dblist

def getDBFields(db,  key,  verbose):
	if key is None:
		raise ValueError('No API Key provided')
	query = {"db" : db}
	fieldlist = runEntrezGetQuery("info",  query,  key,  verbose)
	return fieldlist

def metaSRAQuery(query, endpoint, verbose):
  #http://metasra.biostat.wisc.edu/api.html
  endpoints = {"sample" : "samples.json", "terms" : "terms"}
  baseURL="http://metasra.biostat.wisc.edu/api/v01/samples.json?"

  if endpoint not in endpoints:
    raise ValueError('Incorrect endpoint requested')

  if isinstance(query, dict):
    results = requests.get(baseURL + endpoints[endpoint], params = query)
    if results.status_code == results.code.ok:
      return results.json()
    else:
      results.raise_for_status()
  else:
    raise ValueError('Query is not a python dictionary')

def sample2run(key,sampleid, verbose):
  srrlist = []
  #Takes a sample ID and will return a list of SRA run IDs
  #https://www.biosstars.org/p/53627/
  samplequery = {"db" : "biosample", "term" : sampleid}
  service = "search"
  sampledata = runEntrezGetQuery(service, samplequery, key, verbose)
  if verbose:
    pprint.pprint(sampledata)

  #Parse the ID from biosample
  biosampleidlist = sampledata['esearchresult']['idlist']
  if verbose:
    for id in biosampleidlist:
      print(id)
  for id in biosampleidlist:
    #link between biosample and SRA
    query = {"dbfrom" : "biosample", "db" : "sra", "id" : id}
    service = "link"
    sradata = runEntrezGetQuery(service, query, key, verbose)
    if verbose:
      pprint.pprint(sradata)
    sraidlist = sradata['linksets'][0]['linksetdbs'][0]['links']
    if verbose:
      for id in sraidlist:
        print(id)
   #Query SRA using the SRA ID
  for id in sraidlist:
    sraquery = {"db" : "sra", "id" : id}
    service = "fetch"
    rundata = runEntrezGetQuery(service, sraquery, key, verbose)
    if verbose:
      pprint.pprint(rundata)

    #Parse the XML for SRR numbers
    tree = et.fromstring(rundata)
    for idnode in tree.findall('.//EXPERIMENT_PACKAGE/RUN_SET/RUN/IDENTIFIERS/PRIMARY_ID'):
      srrlist.append(idnode.text)
  return srrlist

def text2sample(key, searchterm, verbose):
  #Takes a text search term and returns a list of samples associated
  samplelist = []
  #Text query
  textquery = {"db" : "sra", "term" : searchterm}
  service = "search"
  textdata = runEntrezGetQuery(service, textquery, key, verbose)
  vPrint(verbose, textdata)
  idlist = textdata['esearchresult']['idlist']

  #Do a link between sraid and biosample
  #for id in idlist:
  linklist = []
  samplequery = {"dbfrom" : "sra", "db" : "biosample", "id" : idlist}
  service = "link"
  linkdata = runEntrezGetQuery(service, samplequery, key, verbose)
  vPrint(verbose, linkdata)
  for linkset in linkdata['linksets']:
    for linksetdbs in linkset['linksetdbs']:
      for links in linksetdbs['links']:
        linklist.append(links)

  #Go after the sample ids
  query = {"db" : "biosample", "id" : linklist, "retmode" : "xml"}
  service = "fetch"
  sampledata = runEntrezGetQuery(service, query, key, verbose)
  vPrint(verbose, sampledata) 
  samplelist = []
  tree = et.fromstring(sampledata)
  for idnode in tree.findall('.//BioSample/Ids/Id'):
    if idnode.get('db') == 'SRA':
      samplelist.append(idnode.text)
  return samplelist
