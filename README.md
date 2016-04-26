EU Arms Exports Scraper
==============================
The scraper extracts information from the EU arms export reports between 2005 and 2013, which is very hard to read for machines. The automatically extracted information is then stored in different data structures (network, country specific) and file formats (CSV, JSON), which are relevant for the next steps, like network analysis, visualization and statistical analysis. 

This repository provides the code and documentation, and [keeps track of bugs as well as feature requests](https://github.com/OKFNat/armScraper/issues).

- Team: [Gute Taten für gute Daten](http://okfn.at/gutedaten/) project of [Open Knowledge Austria](http://okfn.at/).
- Status: Production
- Documentation: English
- License:
	- Content: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)
	- Software: [MIT License](http://opensource.org/licenses/MIT) 

**Used Software**

The sourcecode is written in Python 2. It was created with use of [iPython](http://ipython.org/), [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/) and [urllib2](https://docs.python.org/2/library/urllib2.html).

## SCRAPER

**Description**

The scraper fetches the html passed in as urls from a csv file and stores them locally. The html is then parsed with BeautifulSoup4. Every table between the requested start country and end country is parsed out row by row, cell by cell and stored into a JSON structure with importing countries -> exporting countries -> arms classes -> data. The data structure is then  used to create nodes and edges files as JSON and CSV. This can also be used to extract country specific data to understand imports and exports from a country's perspective.

**Run scraper**

```
cd code
python arms-scraper.py
```

### How the scraper works
**Configure the Scraper**

There are two global variables in [arms-scraper.py](code/arms-scraper.py) you may want to change to your needs.

- DELAY_TIME: To not overload the server or may get blocked because of too many request, you should set the delay time to fetch to 1-5 seconds, not less.
- TS: The timestamp as a string can be set to the last download. So you can use downloaded data over and over again and must not do it everytime. When you do it first time, you can set the value to ```datetime.now().strftime('%Y-%m-%d-%H-%M')```, so it is the timestamp when the scraper starts.

**Download raw html**

Here all the html raw data gets downloaded, stored locally and the basic data gets parsed.

- Download the overview page with the tables (html). For this, the [data/raw/csv/list-eu-armsexports-reports.csv](data/raw/csv/list-eu-armsexports-reports.csv) spreadshit is needed. It's data structure of is needed for the scraper to know where to start from and what to extract.
	- year: year of the arms export report
	- report-number: number of the arms export report
	- url: url, where the arms export is located
	- div-id: ID of the div, where the tables are in.
	- start-country: first country to extract.
	- end-country: last country to extract.
- Open the downloaded file.
- Parse out the basic information about each lobbying register entry from the overview table. This is necessary here, because the download of the lobbying register entry page needs the link from the Registerzahl field.
- Store the parsed data as JSON file.
- Download all lobbying register entry pages (html) with the unique id as postfix.

**Parse html**

Here the description of the project gets added to the data.

- Open the overview page.
- Parse out the basic information about each lobbying register entry from the overview table. This is necessary here, because the download of the lobbying register entry page needs the link from the Registerzahl field.
- Open all lobbying register entry pages (html).
- Parse out the additional information from all lobbying register pages.
- Store updated data as JSON file.

The lobbying register does not publish the A2 entries, so the scraper never got tested with this and some A2 specific data entries are not part of the parser.

**Export CSV**

Here the data gets exported as a CSV file.
- Open the data (JSON).
- Save the serialized data as CSV file.

## DATA INPUT
The EU publishes their annual arms exports reports as HTML tables in the web. We have so far found the reports from 2005 to 2013, which we built this scraper for. 

**Important: The data on the website has changed during our work, so the links to the annual arms export reports we used do not work anymore.**

### The Table
The tables are the basic matrix with the data available. They all look the same: on the left you see the exporting countries Austria and Spain and on the top the importing country Afghanistan, which the table is for. e. g. Austria applied for 3 licenses to Afghanistan in CML 1, which most likely were some Glocks.

**Example**

                   Afghanistan  		     
|	  |    | ML1	| ML12	| ML20     | Total   |
|-----|----|--------|-------|----------|---------|
| Austria | a | 3      | 	|          |         |
| 	  | b  | 13367  | 	|          |         |
| 	  | c  | 	| 	|          |         |
| Spain	  | a | 	| 1	| 15       | 16	     |
| 	  | b  | 	| 38723 | 6977138  | 7015861 |
| 	  | c  | 	| 	|          | 	     |
| Total	  | a | 3	| 1	| 15       | 19	     |
| 	  | b  | 13367	| 38723	| 6977138  | 7029228 |
| 	  | c  | 	| 	|   	   |   	     |

**EU Common Military List categories**

The second row is an EU specific classification of arms, the [EU Common Military List categories]](http://eur-lex.europa.eu/legal-content/DE/TXT/?uri=OJ%3AC%3A2014%3A107%3AFULL).

- ML1: Smooth-bore weapons with a calibre of less than 20 mm, other arms and automatic weapons with a calibre of 12,7 mm (calibre 0,50 inches) or less and accessories, and specially designed components therefor.
- ML2: Smooth-bore weapons with a calibre of 20 mm or more, other weapons or armament with a calibre greater than 12,7 mm (calibre 0,50 inches), projectors and accessories, and specially designed components therefor.
- ML3: Ammunition and fuze setting devices, and specially designed components therefor.
- ML4: Bombs, torpedoes, rockets, missiles, other explosive devices and charges and related equipment and accessories, specially designed for military use, and specially designed components therefor.
- ML5: Fire control, and related alerting and warning equipment, and related systems, test and alignment and countermeasure equipment, specially designed for military use, and specially designed components and accessories therefor.
- ML6: Ground vehicles and components.
- ML7: Chemical or biological toxic agents, ‘tear gases’, radioactive materials, related equipment, components, materials and ‘technology’
- ML8: ‘Energetic materials’, and related substances.
- ML9: Vessels of war, special naval equipment and accessories, and components therefor, specially designed for military use.
- ML10: ‘Aircraft’, unmanned airborne vehicles, aero-engines and ‘aircraft’ equipment, related equipment and components, specially designed or modified for military use.
- ML11: Electronic equipment, not controlled elsewhere on the EU Common Military List, specially designed for military use and specially designed components therefor.
- ML12: High velocity kinetic energy weapon systems and related equipment, and specially designed components therefor:
- ML13: Armoured or protective equipment and constructions and components:
- ML14: Specialised equipment for military training or for simulating military scenarios, simulators specially designed for training in the use of any firearm or weapon controlled by ML1 or ML2, and specially designed components and accessories therefor.
- ML15: Imaging or countermeasure equipment, specially designed for military use, and specially designed components and accessories therefor.:
- ML16: Forgings, castings and other unfinished products the use of which in a controlled product is identifiable by material composition, geometry or function, and which are specially designed for any products controlled by ML1 to ML4, ML6, ML9, ML10, ML12 or ML19.
- ML17: Miscellaneous equipment, materials and libraries, and specially designed components therefor.
- ML18: Equipment for the production of products referred to in the EU Common Military List.
- ML19: Directed energy weapon systems (DEW), related or countermeasure equipment and test models, and specially designed components therefor.
- ML20: Cryogenic and ‘superconductive’ equipment, and specially designed components and accessories therefor.
- ML21: ‘Software’ specially designed or modified for the ‘development’, ‘production’‘use’ of equipment or materials controlled by the EU Common Military List.
- ML22: ‘Technology’ for the ‘development’, ‘production’ or ‘use’ of items controlled in the EU Common Military List, other than that ‘technology’ controlled in ML7. 

**Keys**

- (a) = number of licences issued (scraper data model => num-licenses)
- (b) = value of licences issued in Euros (scraper data model => val-licenses)
- (c) = value of arms exports in Euros (if available) (scraper data model => val-arms)
- (d) = total EU number of licence refusals (small discrepancies may appear between breakdowns and totals due to denials concerning more than one ML item or denials for items other than those appearing in the ML) (scraper data model => total-eu-licenses-refusals)
- (e) = criteria numbers on which refusals are based (the approximate number of times each criterion is invoked is indicated in brackets) (scraper data model => criteria-numbers)

**Corrections in raw html**

In some HTML tables were errors, which were corrected manually after downloading the html files cause it was easier than coding a proper function in the scraper.

### Soundness
- "Statistics are compiled differently by each Member State: no uniform standard is used. Consequently, owing to current procedures regarding arms export reporting or data protection legislation, not all countries have been able to submit the same information (3):"
- "With regard to actual exports authorised by EU Member States (row (c)), it is important to note that Belgium, Denmark, Germany, Poland, Greece, Ireland and the United Kingdom could not provide these data while France and Italy have reported total values only. No aggregation is therefore reported at the EU level."

For more corrections of data, look at the specific reports below.

### 16th Report - 2013  
[Original HTML](http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52015XG0327(05)&rid=1)

**raw data correction**

- Taiwan: "a", "b", "c" were missing in Finland rows

### 15th Report - 2012
[Original HTML](http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52014XG0121(01)&rid=4)

**raw data correction**

- Pakistan: In Total rows:
	- delete "d"
	- exchange "e" to "d"
	- last row gets "e"

### 14th Report - 2011
[Original HTML](http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52012XG1214(01)&rid=7)

**raw data correction**
No errors.

### 13th Report - 2010
[Original HTML](http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52011XG1230(01)&rid=6)

**raw data correction**
- India: merged two paragraphs into on in "Total" row
- Israel: merged two paragraphs into on in "Total" row
- Syria: merged two paragraphs into on in "Total" row
- Turkmenistan: merged two paragraphs into on in "Total" row

### 12th Report - 2009
[Original HTML](http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52011XG0113(01)&rid=1)

**raw data correction**

No errors.

### 11th Report - 2008
[Original HTML](http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52009XG1106(01)&rid=1)

**raw data correction**

No errors.

### 10th Report - 2007
**SO FAR, THE SCRAPER DOES NOT WORK FOR THE 1ßth REPORT**

[Original HTML](http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52008XG1122(01)&rid=1)

**raw data correction**
- Kenya: add "a" and "b" Poland rows

### 9th Report - 2006
**SO FAR, THE SCRAPER DOES NOT WORK FOR THE 9th REPORT**

[Original HTML](http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52007XG1026(01)&rid=1)

**raw data correction**

### 8th Report - 2005
[Original HTML](http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52005XG1223(03)&rid=1)

**raw data correction**
- Switzerland: In second table span around country name is missing => ```<span class="bold">SWITZERLAND</span>```

## DATA OUTPUT

**raw html**

```
<html>
  <head>
  <body>
    .
    <div id="C_2015103EN.01000601">
      . 
      <p id="d1e590-6-1-table" class="ti-tbl">		=> header for table
      <table class="table">				=> table
		<colgroup>
		<tbody>
		  <tr class="table">				=> row
		    <td class="table">
		      <p class="tbl-txt">				=> cell
		    <td class="table">
		  .
		  <tr class="table">
		    <td class="table">
		      <p class="tbl-txt">
		    <td class="table">
	      <p>
	      .
	      <p id="d1e1391-6-1-table" class="ti-tbl">
	      <table class="table">
	      <table class="table">				=> table
		<colgroup>
		<tbody>
		  <tr class="table">				=> row
		    <td class="table">
		      <p class="tbl-txt">				=> cell
		    <td class="table">
		  .
		  <tr class="table">
		    <td class="table">
		      <p class="tbl-txt">
		    <td class="table">
	      <p>
	</div>
  </body>
  </head>
</html>
```

Because each html report has additional tables in after the ones we want, we have to define a stop country in the [data/raw/csv/list-eu-armsexports-reports.csv](data/raw/csv/list-eu-armsexports-reports.csv)

**arms exports data as JSON**
```
{
	"YEAR" (string) {
		<COUNTRY-DESTINATION> (string) {
			"Total": {
				"num-licenses": int
				"val-licenses": int
				"val-arms": int
				"total-eu-licenses-refusals": int
				"criteria-numbers": int
			}
			"CML1": {
				"num-licenses": int
				"val-licenses": int
				"val-arms": int
				"total-eu-licenses-refusals": int
				"criteria-numbers": int
			}
			.
			"CML22": {
				"num-licenses": int
				"val-licenses": int
				"val-arms": int
				"total-eu-licenses-refusals": int
				"criteria-numbers": int
			}
			<COUNTRY-ORIGIN> (string) {
				"Total": {
					"num-licenses": int
					"val-licenses": int
					"val-arms": int
					"total-eu-licenses-refusals": int
					"criteria-numbers": int
				}
				"CML1": {
					"num-licenses": int
					"val-licenses": int
					"val-arms": int
					"total-eu-licenses-refusals": int
					"criteria-numbers": int
				}
				.
				"CML22": {
					"num-licenses": int
					"val-licenses": int
					"val-arms": int
					"total-eu-licenses-refusals": int
					"criteria-numbers": int
				}
			}
		}
	}
}
```

**arms export data as CSV**
- unique-id
- year
- importing-country
- exporting-country
- CML-category
- num-licenses-imported
- val-licenses-imported
- val-arms-imported
- total-eu-licenses-refusals-imported
- criteria-numbers-imported

Each row is one export in one year.

## CONTRIBUTION

In the spirit of free software, everyone is encouraged to help improve this project.

Here are some ways you can contribute:

- by reporting bugs
- by suggesting new features
- by translating to a new language
- by writing or editing documentation
- by analyzing the data
- by visualizing the data
- by writing code (**no pull request is too small**: fix typos in the user interface, add code comments, clean up inconsistent whitespace)
- by refactoring code
- by closing issues
- by reviewing pull requests
- by enriching the data with other data sources

When you are ready, submit a [pull request](https://github.com/OKFNat/armScraper/pulls).

### Submitting an Issue

We use the [GitHub issue tracker](https://github.com/OKFNat/armScraper/issues) to track bugs and features. Before submitting a bug report or feature request, check to make sure it hasn't already been submitted. When submitting a bug report, please try to provide a screenshot that demonstrates the problem. 

## COPYRIGHT
All content is openly licensed under the [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/) license, unless otherwisely stated.

All sourcecode is free software: you can redistribute it and/or modify it under the terms of the MIT License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Visit [http://opensource.org/licenses/MIT](http://opensource.org/licenses/MIT) to learn more about the MIT License.


## SOURCES

**Arms Exports**
- [SIPRI](http://sipri.org/): Stockholm International Peace Research Institute
- [Department of Peace and Conflict Research, Uppsala University](http://www.pcr.uu.se/)
- [Small Arms Survey](http://www.smallarmssurvey.org/)
- [The Review of the EU common position on arms exports: prospects for strenghtened controls](http://www.sipri.org/research/disarmament/eu-consortium/publications/publications/non-proliferation-paper-7): SIPRI, 2012
- [The Limitations of European Union Reports on Arms Exports: The Case of Central Asia](http://www.nonproliferation.eu/web/documents/other/paulholtomandmarkbromley4e9eaf8345077.pdf): SIPRI, 2010.
- [The European Union Code of Conduct on Arms Exports: Improving the Annual Report](http://books.sipri.org/files/PP/SIPRIPP08.pdf): Sibylle Bauer and Mark Bromley - SIPRI, 2004.
- [EU Annual Report](http://www.sipri.org/research/armaments/transfers/transparency/EU_reports): SIPRI page.

**Documentation**
- [Common military list of the European Union (pdf)](http://eur-lex.europa.eu/legal-content/DE/TXT/?uri=OJ%3AC%3A2014%3A107%3AFULL)
- [The European Union Code of Conduct on Arms Exports](http://www.consilium.europa.eu/uedocs/cmsUpload/08675r2en8.pdf)
- [European Union External Action: Arms Export Control](http://www.eeas.europa.eu/non-proliferation-and-disarmament/arms-export-control/index_en.htm)

**Other datasources**
- [SIPRI](http://www.sipri.org/databases)
- [Armed Conflict Location & Event Data Project](http://www.acleddata.com/)
- [Uppsala Conflict Data Programm](http://www.pcr.uu.se/research/ucdp/datasets/)

**Media coverage**
- [derstandard.at: Wie viele Waffen Österreich an Saudi-Arabien lieferte](http://derstandard.at/2000029272616/Wie-viele-Waffen-Oesterreich-nach-Saudi-Arabien-lieferte)
- [NZZ.at: Der Arabische Frühling und die europäischen Waffenbauer](https://nzz.at/republik/der-arabische-fruehling-und-die-europaeischen-waffenbauer)

## REPOSITORY
- [README.md](README.md): Overview of repository
- [code/arms-scraper.py](code/arms-scraper.py): scraper
- [CHANGELOG.md](CHANGELOG.md)
- [LICENSE](LICENSE)

## CHANGELOG
### Version 0.2 - 2016-04-26
- update documentation
- add 2006 and 2007 scraper
- update CSV export
- implement data model in readme
- add license, changelog and .gitignore
