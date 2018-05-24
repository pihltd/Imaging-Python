#!/usr/bin/env python

import entrezStuff as entrez
import pprint
import argparse
import xml.etree.ElementTree as et


def newSRASearch(query):
	baseURL = "https://www.ncbi.nlm.nih.gov/Traces/sdl/1/retrieve?"

def parseFetchXMLForRunIDs(xmldoc, verbose):
	
	if verbose:
		pprint.pprint(xmldoc)
	tree = et.fromstring(xmldoc)
	#for node in tree.iter():
	#	print node.tag, node.text
	
	idlist = []
	#for idnode in tree.findall("EXPERIMENT_PACKAGE_SET/EXPERIMENT_PACKAGE/RUN_SET/RUN/IDENTIFIERS/PRIMARY_ID"):
	for idnode in tree.iter():
		#print( "Node value %s" % idnode.txt)
		if idnode.tag == 'PRIMARY_ID':
			idlist.append(idnode.text)
		
	return idlist
	
	
	
def main(args):
	#Step 1 - Do a search for 1000 Genomes
	service = "search"
	api_key = "c33b6f48dd5fd9feb3dbfcdc282f29719b09"
	query = { 'db' : 'sra','term' : '1000 Genomes', 'retmode' : 'json'}
	thougenomes = entrez.runEntrezGetQuery(service, query, api_key, args.verbose)
	idlist = thougenomes['esearchresult']['idlist']
	if args.test:
		idlist = ['4963657', '4961977']
	for id in idlist:
		print(id)
		service = 'fetch'
		query = {'db' : 'sra', 'id' : id}
		fetchres = entrez.runEntrezGetQuery(service, query, api_key, args.verbose)
		#pprint.pprint(fetchres)
		srrlist = parseFetchXMLForRunIDs(fetchres, args.verbose)
		for srr in srrlist:
			print(srr)
		
	
	#Parse out the IDs?
	
	#Send each ID to fetch?
	#https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?id=4963657&api_key=c33b6f48dd5fd9feb3dbfcdc282f29719b09&db=sra&retmode=json
	#SRR number in <Experiment_Package_Set><Experimient_package><Run_set><Run><Identifiers><Primary_ID>
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", action = "store_true", help = 'Enable verbose feedback.')
	parser.add_argument("-t",  "--test",  action = "store_true",  help = "Run in Test Mode")
	
	args = parser.parse_args()
	main(args)
  

