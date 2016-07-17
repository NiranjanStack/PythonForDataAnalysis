
#Analyzing time zone data of usa.gov 

from pandas import DataFrame, Series
import numpy as np
import json
path = 'usagov_data.txt'
records = [json.loads(line) for line in open(path)]

#count time zone
time_zones = [rec['tz'] for rec in records if 'tz' in rec]

def get_counts(seq):
	counts = {}
	for x in seq:
		if x in counts:
			counts[x] += 1
		else:
			counts[x] = 1
	return counts
	
counts = get_counts(time_zones)

counts['America/New_York']

#Top 10 time zones and their counts
def top_counts(count_dict, n=10):
	value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
	value_key_pairs.sort()
	return value_key_pairs[-n:]

top_counts(counts)

#Alternate method using numpy
from collections import Counter
counts = Counter(time_zones)
counts.most_common(10)

#Count tz using Pandas
from pandas import DataFrame, Series
import pandas as pd
frame = DataFrame(records)

frame['tz'][:10]

tz_counts = frame['tz'].value_counts()

tz_counts[:10]

#Plotting the data
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()

tz_counts[:10]

#plot
tz_counts[:10].plot(kind='barh', rot=0)

frame['a'][20]

#Splitting data
results = Series([x.split()[0] for x in frame.a.dropna()])  # 'a' is column name
results.value_counts()[:10]

#decompose the top time zones into Windows and non-Windows users.
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
operating_system[:10]

#group the data by its time zone column and OS
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
agg_counts[:10]

#select the top overall time zones
indexer = agg_counts.sum(1).argsort()
indexer[:10]

#use take to select the rows in that order, then slice off the last 10 rows:
count_subset = agg_counts.take(indexer)[:10]
count_subset

#Plots
count_subset.plot(kind='barh', stacked='True')

normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked='True')






