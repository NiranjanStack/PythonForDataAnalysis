#Pull XML data into python

from lxml import objectify
from pandas import DataFrame

path = 'Books.xml'
parsed = objectify.parse(open(path))
root = parsed.getroot()

#root.INDICATOR return a generator yielding each <INDICATOR> XML element. For each
#record, we can populate a dict of tag names (like YTD_ACTUAL) to data values
data = []
skip_fields = ['description']
for books in root.book:
	book_list = {}
	for child in books.getchildren():
		if child.tag in skip_fields:
			continue
		book_list[child.tag] = child.pyval
	data.append(book_list)

#Lastly, convert this list of dicts into a DataFrame:
allbooks = DataFrame(data)

allbooks
