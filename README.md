EU arms exports scraper
==============================
The scraper extracts information from the EU arms export reports between 2005 and 2013, which is very hard to read for machines. The automatically extracted information is then stored in different data structures (network, country specific) and file formats (CSV, JSON), which are relevant for the next steps, like network analysis, visualization and statistical analysis. 

- Team: Gute Taten für gute Daten Project (Open Knowledge Austria)
- Status: Prototype
- Documentation: English
- License: [MIT License](http://opensource.org/licenses/MIT)
- Website: [Gute Taten für gute Daten project](http://okfn.at/gutedaten/) 

**Used Software**
- [iPython](http://ipython.org/) with [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/)

## SCRAPER

**Description**

The scraper fetches the html passed in as urls from a csv file and stores them locally. The html is then parsed with BeautifulSoup4. Every table between the requested start country and end country is parsed out row by row, cell by cell and stored into a JSON structure with importing countries -> exporting countries -> arms classes -> data. The data structure is then  used to create nodes and edges files as JSON and CSV. This can also be used to extract country specific data to understand imports and exports from a country's perspective.

**Run scraper**

```
cd code
python eu-arms.py
```

## Used Data
The EU publishes their annual arms exports reports as HTML tables in the web. We have so far found the reports from 2005 to 2013, which we built this scraper for. 

### The Table
The tables are the basic matrix with the data available. They all look the same: on the left you see the exporting countries Austria and Spain and on the top the importing country Afghanistan, which the table is for. e. g. Austria applied for 3 licenses to Afghanistan in CML 1, which most likely were some Glocks.

Afghanistan
|	  |    | ML1	| ML12	| ML20     | Total   |
|---------|----|--------|-------|----------|---------|
| Austria | a  | 3      | 	|          |         |
| 	  | b  | 13367  | 	|          |         |
| 	  | c  | 	| 	|          |         |
| Spain	  | a  | 	| 1	| 15       | 16	     |
| 	  | b  | 	| 38723 | 6977138  | 7015861 |
| 	  | c  | 	| 	|          | 	     |
| Total	  | a  | 3	| 1	| 15       | 19	     |
| 	  | b  | 13367	| 38723	| 6977138  | 7029228 |
| 	  | c  | 	| 	|   	   |   	     |

**EU Common Military List categories**

The second row is an [EU specific classificationi of arms](EU Common Military List categories).
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

In some HTML tables were errors, which were corrected manually after downloading the html files.

### Soundness
- "Statistics are compiled differently by each Member State: no uniform standard is used. Consequently, owing to current procedures regarding arms export reporting or data protection legislation, not all countries have been able to submit the same information (3):"
- "With regard to actual exports authorised by EU Member States (row (c)), it is important to note that Belgium, Denmark, Germany, Poland, Greece, Ireland and the United Kingdom could not provide these data while France and Italy have reported total values only. No aggregation is therefore reported at the EU level."

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

## CREATED DATA
- [data-model.md](data-model.md): Describes the data structure used and created

## STRUCTURE
- [README.md](README.md): Overview of repository
- [data-model.md](data-model.md): Describes the data structure used and created

## TODO
**must**
- verify the data: check in each report
	- check country with two tables
	- check country name with two words
	- check first and last table
	- check 3 tables in depth
	- check with different country name structure: before table, first row, second row
- check files for network analyses with Gephi or networkX python module

**optional**
- update code to Python3
- csv files for network analysis with all years in it
- compare total values with sum of single values

**new features**
- analyze and visualize the data: networkX, maps, Gephi
- parse aggregated tables and compare with data from country level
- combine with data from SIPRI
- add country namecodes for easier enrichment with other data
- visualize on a map the flows of arms and centrality of countries

## OUTREACH
- [derstandard.at: Wie viele Waffen Österreich an Saudi-Arabien lieferte](http://derstandard.at/2000029272616/Wie-viele-Waffen-Oesterreich-nach-Saudi-Arabien-lieferte)
- [NZZ.at: Der Arabische Frühling und die europäischen Waffenbauer](https://nzz.at/republik/der-arabische-fruehling-und-die-europaeischen-waffenbauer)

## CHANGELOG
### Version 0.1 - 2015-10-29
**init repo**
- parse reports 2005 and 2008-2013
- parse html tables
- save reports in one json and one for each year with lists of importing and exporting countries 
- save reports in nodes and edges csv for each year
- save country specific data for imports and exports in csv files

