#!/usr/bin/env python

import entrezStuff as entrez
import pprint
import argparse
import xml.etree.ElementTree as et
import requests


def newSRASearch(query):
	baseURL = "https://www.ncbi.nlm.nih.gov/Traces/sdl/1/retrieve?"

def parseFetchXMLForRunIDs(xmldoc, idlist, verbose):
	
	if verbose:
		pprint.pprint(xmldoc)
	tree = et.fromstring(xmldoc)
	for idnode in tree.findall('.//EXPERIMENT_PACKAGE/RUN_SET/RUN/IDENTIFIERS/PRIMARY_ID'):
		if verbose:
			print ("Node value %s\tNode value:\t%s" % (idnode.tag, idnode.text))
		idlist.append(idnode.text)
	
def sddpQuery(query, endpoint, verbose):
	validendpoints = ['retrieve', 'locality']
	if endpoint not in validendpoints:
		print (("%s is not a valid SDDP endpoint") % endpoint)
	baseURL = "https://www.ncbi.nlm.nih.gov/Traces/sdl/1/"
	url = baseURL + endpoint
	data = requests.get(url,  params=query)
	if verbose:
		pprint.pprint(data.url)
		pprint.pprint(data.status_code)
		pprint.pprint(data.json())
	return data.json()
    
	
def main(args):
	#Step 1 - Do a text query
	service = "search"
	api_key = "c33b6f48dd5fd9feb3dbfcdc282f29719b09"
	if args.project == '1kgenomes':
		query = { 'db' : 'sra','term' : '1000 Genomes', 'retmode' : 'json'}
	elif args.project == 'topmed':
		query = { 'db' : 'sra','term' : 'topmed', 'retmode' : 'json'}
	thougenomes = entrez.runEntrezGetQuery(service, query, api_key, args.verbose)
	idlist = thougenomes['esearchresult']['idlist']
	
	#Use the returned IDs to query SRA for the associated information
	# The "fetch" routine only returns XML, not JSON.
	if args.test:
		if args.project == '1kgenomes':
			idlist = ['4963657', '4961977']
		elif args.project == 'topmed':
			idlist = ['4499923', '4499924']
	
	srrlist = []
	for id in idlist:
		print(id)
		service = 'fetch'
		query = {'db' : 'sra', 'id' : id}
		fetchres = entrez.runEntrezGetQuery(service, query, api_key, args.verbose)
		
		#Parse the returned XML to get the Run identifiers
		parseFetchXMLForRunIDs(fetchres, srrlist, args.verbose)
		
	if args.verbose:
		for srr in srrlist:
			print(srr)
			
	#Query the SDDP Location endpoint for info on each of the run identifiers
	if args.test:
		if args.project == '1kgenomes':
			srrlist = ['SRR6487745', 'SRR6486455']
		elif args.project == 'topmed':
			srrlist = ['SRR6062248', 'SRR6062553']
	for srr in srrlist:
		endpoint = 'locality'
		query = {"acc" : srr, 'type' : 'sra_files'}
		jsondata = sddpQuery(query, endpoint, args.verbose)
		for filedata in jsondata:
			if 'files' not in filedata:
				print (("ID:\t%s\tError:\t%s\n") % (filedata['accession'],filedata['message']))
			else:
				for seqfile in filedata['files']:
					filelocation = seqfile['locality'][0]['service']
					filetype = seqfile['type']
					print (("ID:\t%s\tLocation:\t%s\tType:\t%s\n") % (srr,filelocation,filetype))		
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
	parser.add_argument("-t",  "--test",  action = "store_true",  help = "Run in Test Mode")
	programchoice = ["1kgenomes", "topmed"]
	parser.add_argument("-p", "--project", required = True, type = str.lower, choices = programchoice, help = "Program  (1kgenomes, topmed) that the tests will be run on")
	
	args = parser.parse_args()
	main(args)
  

