#Pulling tabular data from website in python

from lxml.html import parse
from urllib2 import urlopen
from pandas import DataFrame

#parsed = parse(urlopen('http://www.uspto.gov/web/offices/ac/ido/oeip/taf/us_stat.htm'))
parsed = parse(urlopen('http://finance.yahoo.com/q/op?s=AAPL+Options'))
doc = parsed.getroot()

links = doc.findall('.//a')
lnk = links[2]

#gets the link name
lnk.get('href')

#for the display text
lnk.text_content()

#gets all urls
urls = [lnk.get('href') for lnk in doc.findall('.//a')]
#urls[:10]

tables = doc.findall('.//table')

#find the tables from website, check with different indexes to find table from website
#a single webpage can have multiple tables

tab1 = tables[3]
tab2 = tables[2]

#Each table has a header row followed by each of the data rows:
rows = tab1.findall('.//tr')

#For the header as well as the data rows, we want to extract the text from each cell; 
#in the case of the header these are th cells and td cells for the data
def _unpack(row, kind='td'):
	elts = row.findall('.//%s' % kind)
	return [val.text_content() for val in elts]

#this returns
#_unpack(rows[0], kind='th')	#header

#_unpack(rows[1], kind='td')	#data at row 1

#Convert all data to dataframe
from pandas.io.parsers import TextParser

def parse_options_data(table):
	rows = table.findall('.//tr')
	header = _unpack(rows[0], kind='th')
	data = [_unpack(r) for r in rows[1:]]
	return TextParser(data, names=header).get_chunk()

tab1_data = parse_options_data(tab1)
tab2_data = parse_options_data(tab2)


	

