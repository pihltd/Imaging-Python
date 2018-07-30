#!/usr/bin/env python

import entrezStuff as entrez
import pprint
import argparse
import requests
import pprint
import os

def main(args):
	#Step 1 - esearch query of dbGaP for the project name
	service = "search"
	api_key = os.environ['NCBIAPIKEY']
	if args.project == '1kgenomes':
		query = { 'db' : 'sra','term' : '1000 Genomes', 'retmode' : 'json'}
	elif args.project == 'topmed':
		query = { 'db' : 'gap','term' : 'topmed', 'retmode' : 'json'}
		
	try:
		dbgapSearch = entrez.runEntrezGetQuery(service, query, api_key, args.verbose)
	except HTTPError as exception:
		pprint.pprint(exception)
	except ValueError as exception:
		pprint.pprint(exception)
		
	idlist = dbgapSearch['esearchresult']['idlist']
	
	if args.test:
		if args.project == '1kgenomes':
			idlist = ['1883637', '1797240']
		elif args.project == 'topmed':
			idlist = ['1888048', '1888024']
			
	#Step 2 - esummary search of dbGaP using IDs from step 1
	service = 'summary'
	phslist = []
	for id in idlist:
		query = {'db' : 'gap', 'id' : id, 'retmode' : 'json'}
		try:
			dbgapSummary = entrez.runEntrezGetQuery(service, query, api_key, args.verbose)
		except HTTPError as exception:
			pprint.pprint(exception)
		except ValueError as exception:
			pprint.pprint(exception)
			

		projectA = dbgapSummary['result'][id]['d_dataset_results']['d_dataset_id']
		#This is a messy string, so split out the PHS
		projectPHS = projectA.split("&amp")
		phslist.append(projectPHS[0])
		
	#Step 3 - Use esearch in SRA to query the PHS numbers
	for phs in phslist:
		query = {'db' : 'sra', 'term' : phs, 'retmode' : 'json'}
		service = 'search'
		try:
			sraSearch = entrez.runEntrezGetQuery(service, query, api_key, args.verbose)
		except HTTPError as exception:
			pprint.pprint(exception)
		except ValueError as exception:
			pprint.pprint(exception)
			
		idlist = sraSearch['esearchresult']['idlist']

		
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
	parser.add_argument("-t",  "--test",  action = "store_true",  help = "Run in Test Mode")
	programchoice = ["1kgenomes", "topmed"]
	parser.add_argument("-p", "--project", required = True, type = str.lower, choices = programchoice, help = "Program  (1kgenomes, topmed) that the tests will be run on")
	
	args = parser.parse_args()
	main(args)
