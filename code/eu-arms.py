#!/bin/env python2
# -*- coding: utf-8 -*-

"""
Scrapes, re-structures and saves the data from the EU arms exports reports from 2005 to 2013. 
"""

import urllib2
import bs4
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from datetime import datetime
import json
import os
from sets import Set
import csv

__author__ = "Stefan Kasberger"
__copyright__ = "Copyright 2015"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Stefan Kasberger"
__email__ = "mail@stefankasberger.at"
__status__ = "Prototype" # 'Development', 'Production' or 'Prototype'


###    GLOBAL   ###


ROOT_FOLDER = os.path.dirname(os.getcwd()) # sets root folder to one directory up
FOLDER_RAW_HTML = ROOT_FOLDER + '/data/raw/html/'
FOLDER_RAW_CSV = ROOT_FOLDER + '/data/raw/csv/'
FOLDER_JSON = ROOT_FOLDER + '/data/json/'
FOLDER_CSV = ROOT_FOLDER + '/data/csv/'
FILENAME_BASE = 'eu-armsexports'
REPORTS_CSV = ROOT_FOLDER + '/data/raw/csv/list-'+FILENAME_BASE+'-reports.csv'
CML_CATS = ['ML1', 'ML2', 'ML3', 'ML4', 'ML5', 'ML6', 'ML7', 'ML8', 'ML9', 'ML10', 'ML11', 'ML12', 'ML13', 'ML14', 'ML15', 'ML16', 'ML17', 'ML18', 'ML19', 'ML20', 'ML21', 'ML22']
EU_COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'United Kingdom']
ARM_TRADE_TYPES = {
	'a': 'num-licenses',
	'b': 'val-licenses',
	'c': 'val-arms',
	'd': 'total-eu-licenses-refusals',
	'e': 'criteria-numbers'
}
ARMS_TYPE_LIST = ['num-licenses', 'val-licenses', 'val-arms', 'total-eu-licenses-refusals', 'criteria-numbers']
ANALYZE_COUNTRIES = ['Austria', 'Germany']
IMPORT_COUNTRIES = []
EXPORT_COUNTRIES = []
IMPORT_COUNTRY_STASH = ''


###    FUNCTIONS   ###


def SetupEnvironment():
	"""Sets up the folder structure and working environment.
	"""
	if not os.path.exists(FOLDER_RAW_HTML):
		os.makedirs(FOLDER_RAW_HTML)
	if not os.path.exists(FOLDER_RAW_CSV):
		os.makedirs(FOLDER_RAW_CSV)
	if not os.path.exists(FOLDER_JSON):
		os.makedirs(FOLDER_JSON)
	if not os.path.exists(FOLDER_CSV):
		os.makedirs(FOLDER_CSV)


def FetchHtml(url):
	"""Fetches html url via urllib().
	
	Args:
		url: url to fetch
	
	Returns:
		html: html string as unicode
	"""
	response = urllib2.urlopen(url)
	html = response.read().decode('utf-8')
	
	return html


def CleanString(text):
	"""Cleans the text string.
	
	Args:
		text: string to be cleaned
	
	Returns:
		text: cleaned string
	"""
	if text == '' or text == None:
		text = 'na'
	text = text.encode('utf-8')

	return text


def CleanHTML(html):
	"""Cleans the HTML
	
	Args:
		html: html string to be cleaned
	
	Returns:
		html: cleaned html string
	"""
	html = html.replace('&nbsp;', '')
	html = html.replace('&ccedil;', '')

	return html


def Save2File(data, filename):
	"""Saves file on specified place on harddrive.
	
	Args:
		data: string to save
		filename: name of the file
	
	Returns:
		na
	"""
	text_file = open(filename, "w")
	text_file.write(data.decode('utf-8'))
	text_file.close()


def ReadText(filename):
	"""Reads file and returns the text.
	
	Args:
		filename: name of the file
	
	Returns:
		text: content of file as string
	"""
	f = open(filename, 'r')
	text = f.read()

	return text


def ParseDoc(html, year, divID, startCountry, endCountry):
	"""Parses out the needed tables and calls ParseTable() to extract the needed data.
	
	Args:
		html: the full html string.
		year: year of the report
		divID: string of the div box where the tables are in.
		startCountry: string from the first table to parse.
		endCountry: string from the last table to parse.
	
	Returns:
		data: returns dict() with udpated data from ParseTable().
	"""

	# setup
	data = {}
	counter = 0
	counterTables = 0
	endCountryPassed = False

	soup = BeautifulSoup(html)

	# find first tag
	soup = soup.find('div', {'id': divID})

	# get all tables
	tables = soup.find_all('table', class_='table')
	print 'tables found:', str(len(tables))

	# iterate over every table
	for table in tables:

		tableState = 1

		# get import country specific to the report and add to list if not already in
		if year == '2013':
			importCountry = CleanString(table.previous_sibling.previous_sibling.span.string)
		elif year == '2012' or year == '2011':
			trOne = table.find('tr')
			importCountry = CleanString(trOne.span.string).lower().title()
		elif year == '2010' or year == '2009' or year == '2008' or year == '2006':
			# check if table has span in first row (=> country row)
			trs = table.find_all('tr', class_='table')
			lenTRs = len(trs[0].find_all('span', class_='bold'))
			if lenTRs == 1:
				trOne = table.find('tr')
				importCountry = CleanString(trOne.span.string).lower().title()
				IMPORT_COUNTRY_STASH = importCountry
			else: 
				importCountry = IMPORT_COUNTRY_STASH
		elif year == '2007':
			# check if table has span in first row (=> country row)
			trs = table.find_all('tr', class_='table')
			lenTRs = len(trs[0].find_all('p', class_='tbl-hdr'))
			# print trs[0]
			# print table.previous_sibling.previous_sibling.string
			if lenTRs == 1:
				trOne = table.find('tr')
				importCountry = CleanString(trOne.p.string).lower().title()
				IMPORT_COUNTRY_STASH = importCountry
				tableState = 1
			elif table.previous_sibling.previous_sibling.string:
				importCountry = CleanString(table.previous_sibling.previous_sibling.string).lower().title()
				IMPORT_COUNTRY_STASH = importCountry
				tableState = 2
			else: 
				importCountry = IMPORT_COUNTRY_STASH
				tableState = -1
		elif year == '2005':
			trTwo = table.find_all('tr', class_='table')
			trTwo = trTwo[1]
			importCountry = CleanString(trTwo.span.string).lower().title()

		# check if end country has been passed
		if endCountryPassed == True and importCountry != endCountry:
			print 'tables extracted:', counterTables
			break
		
		if importCountry not in IMPORT_COUNTRIES:
			IMPORT_COUNTRIES.append(importCountry)

		# check if you are at the start country in the tables
		if importCountry == startCountry:
			startCountry = 'passed'

		# check if you are at the end country in the tables
		if importCountry == endCountry:
			endCountryPassed = True

		# check if you are after the start country
		if startCountry == 'passed':
			# parse the table values
			data, startCountry, endCountry = ParseTable(data, table, year, importCountry, startCountry, endCountry, tableState)
			counterTables += 1

	print 'Import countries:', len(IMPORT_COUNTRIES)
	print 'Export countries:', len(EXPORT_COUNTRIES)
	return data


def ParseTable(data, table, year, importCountry, startCountry, endCountry, tableState):
	"""Parses out the needed information from the html table and saves it in a dict(). 
	
	Args:
		data: dict() with already parsed data.
		table: BeautifulSoup table object.
		year: year of the report
		importCountry: string with the country of the actual table.
		startCountry: string from the first table to parse.
		endCountry: string from the last table to parse.
		tableState: state of the table row
	
	Returns:
		data: updated data dict() with data from the actual table added to existing data.
		startCountry: string from the first table to parse. 'passed' if the first country has been passed.
		endCountry: string from the last table to parse. 'passed' if the last country has been passed.
	"""

	# setup
	colList = []
	rowCounter = 0
	rowLength = 0
	exportCountry = ''

	# get all rows specific to the report
	if year == '2013' or year == '2012' or year == '2011':
		trs = table.find_all('tr', class_='table')
	elif year == '2010' or year == '2009' or year == '2008' or year == '2007' or year == '2006':
		trs = table.find_all('tr', class_='table')
		lenTRs = len(trs[0].find_all('span', class_='bold'))
		if lenTRs == 1:
			trs = trs[1:]
	elif year == '2007':
		if tableState == 1:
			trs = table.find_all('tr', class_='table')
			trs = trs[1:]
		elif tableState == 2:
			trs = table.find_all('tr', class_='table')
		elif tableState == -1:
			trs = table.find_all('tr', class_='table')
	elif year == '2005':
		trs = table.find_all('tr', class_='table')
		trs = trs[2:]

	# get over each row
	for tr in trs:
		armsKey = ''
		cellCounter = 0
		totalRows = False
		ps = tr.find_all('p')
		
		# get over first row
		if rowCounter == 0 :
			for p in ps:
				if CleanString(p.string) == 'TOTAL per destination':
					colList.append('Total')
				else:
					colList.append(CleanString(p.string).replace(' ', ''))
			if year == '2007' or year == '2005':
				rowLength = len(ps)+1
				colList = colList[1:]
			else:
				rowLength = len(ps)
				colList = colList[2:]
		
		# get over all rows after the first one
		else:
			for p in ps:
				# extract rows with text in first cell
				if len(ps) == rowLength:
					# check if in first cell (export country)
					if cellCounter == 0:

						# check if total row started
						if CleanString(p.string) == 'Total per ML category' or CleanString(p.string) == 'TOTAL PER ML category' or CleanString(p.string) == 'TOTAL per category':
							exportCountry = 'Total'
						# get export country
						else:
							exportCountry = CleanString(p.string)
						
						if importCountry not in data.keys():
							data[importCountry] = {}
						if exportCountry not in EXPORT_COUNTRIES:
							EXPORT_COUNTRIES.append(exportCountry)
						if exportCountry not in data[importCountry].keys():
							data[importCountry][exportCountry] = {}
						
					# check if in second cell (type of export)
					elif cellCounter == 1:
						# correct whitespace bugs of CML in html
						armsKey = CleanString(p.string).replace(" ", "")

					# check if in cell with numbers
					elif CleanString(p.string) != 'na':
						data = ParseCell(data, CleanString(p.string), colList[cellCounter-2], armsKey, importCountry, exportCountry)

				# extract rows without text in first cell
				if len(ps) == rowLength-1:
					
					# check if in second cell (type of export)
					if cellCounter == 0:
						armsKey = CleanString(p.string)
					# check if in cell with numbers
					elif CleanString(p.string) != 'na':
						data = ParseCell(data, CleanString(p.string), colList[cellCounter-1], armsKey, importCountry, exportCountry)

				cellCounter += 1
		rowCounter += 1

	return data, startCountry, endCountry


def ParseCell(data, val, colName, armsKey, importCountry, exportCountry):
	"""Parses out the needed information from the html cell and saves it in a dict(). 
	
	Args:
		data: dict() with already parsed data.
		val: string of cell value.
		colName: name of the column of the table.
		totalRows: True if parser is in a total row at the end of the table.
		armsKey: type of arms export as string.
		importCountry: import country as string.
		exportCountry: export country as string.
	
	Returns:
		data: updated data dict() with data from the actual table cell added to existing data.
	"""
	# check if in a total row
	if exportCountry == 'Total':
		if colName not in data[importCountry].keys():
			data[importCountry][colName] = {}
		data[importCountry][colName][ARM_TRADE_TYPES[armsKey]] = val
	# check if not in total row => everything above
	else:
		# print importCountry, exportCountry, colName, armsKey, val # prints out cell content to be saved in dict()
		if colName not in data[importCountry][exportCountry].keys():
			data[importCountry][exportCountry][colName] = {}
		data[importCountry][exportCountry][colName][ARM_TRADE_TYPES[armsKey]] = val

	return data


def Save4Network(data, year):
	"""Re-structures into network specific format and saves the data from dict() in files for further network analyses.
	
	Args:
		data: dict() with all the data
		year: year of the report
	
	Returns:
		na
	"""

	# SAVE EDGES CSV
	string = '"unique id", "Source", "Target", "category", "num-licenses", "val-licenses", "val-arms", "total-eu-licenses-refusals", "criteria-numbers"\n'
	# string = '"unique id", "exporting-country", "importing-country", "category", "num-licenses", "val-licenses", "val-arms", "total-eu-licenses-refusals", "criteria-numbers"\n'
	# strNetworkX = ''
	# strCountry = ''
	# strGephiCountry = ''
	# strNetworkXCountry = ''

	primaryKey = 1

	# run over all importing countries
	for importCountry in data.keys():
		# run over all exporting countries
		for exportCountry in data[importCountry].keys():
			# filter out total imports and CML's of import countries
			if exportCountry != 'Total' and exportCountry not in CML_CATS:
				# run over all CML's + Total
				for elem in data[importCountry][exportCountry].keys():
					
					string += str(primaryKey)+', "'+exportCountry+'", "'+importCountry+'", "'+elem+'"'

					# check which keys are available and write their values or empty string into the CSV string
					for armType in ARMS_TYPE_LIST:
						if armType in data[importCountry][exportCountry][elem].keys():
							string += ', "'+data[importCountry][exportCountry][elem][armType]+'"'
						else:	
							string += ', '
					string += '\n'
					primaryKey += 1
	# save string to file
	Save2File(string, FOLDER_CSV+ts+'_'+FILENAME_BASE+'_'+year+'_edges.csv')

	# SAVE NODES CSV
	string = '"unique-id", "country", "num-licenses-imported", "val-licenses-imported", "val-arms-imported", "total-eu-licenses-refusals-imported", "criteria-numbers-imported"\n'

	listCountries = Set(IMPORT_COUNTRIES) | Set(EXPORT_COUNTRIES)
	primaryKey = 1

	# run over all countries
	for country in listCountries:
		string += str(primaryKey)+', "'+country+'"'
		# check if country is an import country
		if country in IMPORT_COUNTRIES:
			# get Total values
			if 'Total' in data[country].keys():
				for armType in ARMS_TYPE_LIST:
					if armType in data[country]['Total'].keys():
						string += ', "'+data[country]['Total'][armType]+'"'
					else:	
						string += ', '
		string += '\n'
		primaryKey += 1
	# save string to file
	Save2File(string, FOLDER_CSV+ts+'_'+FILENAME_BASE+'_'+year+'_nodes.csv')


def SaveCountry(data, country):
	"""Re-structures into country specific format and saves the data from dict() in files for further analyses.
	
	Args:
		data: dict() with all the data
		country: country to extract
	
	Returns:
		na
	"""

	# setup environment
	if not os.path.exists(FOLDER_CSV+country+'/'):
		os.makedirs(FOLDER_CSV+country+'/')

	# save exports to other countries
	primaryKey = 1
	string = '"unique-id", "year", "exported-to", "category", "num-licenses-imported", "val-licenses-imported", "val-arms-imported", "total-eu-licenses-refusals-imported", "criteria-numbers-imported"\n'

	# run over every year
	for year in data.keys():
		# run over all importing countries
		for importCountry in data[year].keys():
			# check if exporting country is the one we look for
			if country in data[year][importCountry].keys():
				# run over all CML's + Total
				for elem in data[year][importCountry][country].keys():
							
					string += str(primaryKey)+', "'+year+'", "'+importCountry+'", "'+elem+'"'

					# check which keys are available and write their values or empty string into the CSV string
					for armType in ARMS_TYPE_LIST:
						if armType in data[year][importCountry][country][elem].keys():
							string += ', "'+data[year][importCountry][country][elem][armType]+'"'
						else:	
							string += ', '
					string += '\n'
					primaryKey += 1
					
	# save string to file
	Save2File(string, FOLDER_CSV+country+'/'+ts+'_'+FILENAME_BASE+'_exports.csv')

	# save imports from other countries
	primaryKey = 1
	string = '"unique-id", "year", "imported-from", "category", "num-licenses-imported", "val-licenses-imported", "val-arms-imported", "total-eu-licenses-refusals-imported", "criteria-numbers-imported"\n'

	# run over all years
	for year in data.keys():
		# check if importing country is the one we are looking for
		if country in data[year].keys():
			# run over all exporting countries
			for exportCountry in data[year][country].keys():
				# filter out CML_CATS and Total of import country 
				if exportCountry not in CML_CATS and exportCountry != 'Total':
					# run over all CML_CATS and Total inside export country
					for elem in data[year][country][exportCountry].keys():
							
						string += str(primaryKey)+', "'+year+'", "'+exportCountry+'", "'+elem+'"'

						# check which keys are available and write their values or empty string into the CSV string
						for armType in ARMS_TYPE_LIST:
							if armType in data[year][country][exportCountry][elem].keys():
								string += ', "'+data[year][country][exportCountry][elem][armType]+'"'
							else:	
								string += ', '
						string += '\n'
						primaryKey += 1

	# save string to file
	Save2File(string, FOLDER_CSV+country+'/'+ts+'_'+FILENAME_BASE+'_imports.csv')


###    MAIN   ###


if __name__ == "__main__":

	DOWNLOAD_FILES = False
	PARSE_FILES = True
	STRUCTURE_DATA = True
	SAVE_COUNTRIES = True

	# setup
	reports = {}
	euArms = {}
	SetupEnvironment()

	startTime = datetime.now()
	# ts = startTime.strftime('%Y-%m-%d-%H-%M')
	ts = '2015-10-28-14-59'
	print 'start:',ts

	# read out reports.csv
	with open(REPORTS_CSV, 'r') as csvfile:
		rows = csv.reader(csvfile, delimiter=',', quotechar='"')
		rows.next()
		# run over each report
		for row in rows:
			year = row[0]
			reportNumber = row[1]
			url = row[2]
			divID = row[3]
			startCountry = row[4]
			endCountry = row[5]
			
			IMPORT_COUNTRIES = []
			EXPORT_COUNTRIES = []
			euArms[year] = {}

			print row
			
			if DOWNLOAD_FILES:
				rawHTML = FetchHtml(url)
				html = CleanHTML(rawHTML)
				Save2File(html, FOLDER_RAW_HTML+ts+'_'+FILENAME_BASE+'_'+year+'.html')

			if PARSE_FILES:
				html = ReadText(FOLDER_RAW_HTML+ts+'_'+FILENAME_BASE+'_'+year+'.html') # html as string
				euArms[year] = ParseDoc(html, year, divID, startCountry, endCountry)
				Save2File(json.dumps(euArms, indent=2, ensure_ascii=True, sort_keys=True), FOLDER_JSON+ts+'_'+FILENAME_BASE+'.json')
				Save2File(json.dumps(euArms[year], indent=2, ensure_ascii=True, sort_keys=True), FOLDER_JSON+ts+'_'+FILENAME_BASE+'_'+year+'.json')
				Save2File(json.dumps(IMPORT_COUNTRIES, indent=2, ensure_ascii=True, sort_keys=True), FOLDER_JSON+ts+'_'+FILENAME_BASE+'_'+year+'_importcountries.json')
				Save2File(json.dumps(EXPORT_COUNTRIES, indent=2, ensure_ascii=True, sort_keys=True), FOLDER_JSON+ts+'_'+FILENAME_BASE+'_'+year+'_exportcountries.json')

			if STRUCTURE_DATA:
				euArms[year] = json.loads(ReadText(FOLDER_JSON+ts+'_'+FILENAME_BASE+'_'+year+'.json'))
				IMPORT_COUNTRIES = json.loads(ReadText(FOLDER_JSON+ts+'_'+FILENAME_BASE+'_'+year+'_importcountries.json'))
				EXPORT_COUNTRIES = json.loads(ReadText(FOLDER_JSON+ts+'_'+FILENAME_BASE+'_'+year+'_exportcountries.json'))
				Save4Network(euArms[year], year)

	if SAVE_COUNTRIES:
		euArms = json.loads(ReadText(FOLDER_JSON+ts+'_'+FILENAME_BASE+'.json')) 
		for country in ANALYZE_COUNTRIES:
			SaveCountry(euArms, country)

	print 'runtime:', (datetime.now() - startTime)
