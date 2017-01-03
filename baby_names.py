# Analyzing Baby Names

import pandas as pd
names1880 = pd.read_csv('F:\\Dropbox\\NiranjanStack\\PythonDataAnalysis\\yob1880.txt', names=['name', 'sex', 'births'])
names1880.groupby('sex').births.sum()

####   __fixes if sum=0 	########################################################
##
##		>>> sum = 0 # oops! shadowed a builtin!
##		>>> sum(l)
##		Traceback (most recent call last):
##		  File "<stdin>", line 1, in <module>
##		TypeError: 'int' object is not callable
##		>>> import sys
##		>>> sum = sys.modules['__builtin__'].sum # -- fixing sum
##		>>> sum(l)
##		6
###############################################################################
,
#consolidating data from all file into 1 & adding birth yead to all of them
years = range(1880,2011)
pieces = []
columns = ['name','sex','births']
for year in years:
	path = 'F:\\Dropbox\\python\\Python for data analysis Wes\\pydata-book-master\\ch02\\names\\yob%d.txt' % year
	frame = pd.read_csv(path, names=columns)
	frame['year'] = year
	pieces.append(frame)
	
# Concatenate everything into a single DataFrame
names = pd.concat(pieces, ignore_index=True)

total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)
total_births.tail()

#plot
total_births.plot(title='Total births by sex & year')

#insert a column prop with the fraction of babies given each name relative to
#the total number of births. A prop value of 0.02 would indicate that 2 out of every 100
#babies was given a particular name.
def add_prop(group):
	births = group.births.astype(float)
	group['prop'] = births / births.sum()
	return group
names = names.groupby(['year','sex'].apply(add_prop))

np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

#extract a subset of the data to facilitate further
#analysis: the top 1000 names for each sex/year combination
def get_top1000(group):
	return group.sort_values(by='births', ascending=False)[:1000]
grouped = names.groupby(['year','sex'])
top1000 = grouped.apply(get_top1000)

#If you prefer a do-it-yourself approach, you could also do:
pieces = []
for year, group in names.groupby(['year', 'sex']):
	pieces.append(group.sort_index(by='births', ascending=False)[:1000])
top1000 = pd.concat(pieces, ignore_index=True)

#Analyzing Naming Trends
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]

#plot
subset.plot(subplots=True, figsize=(12,10), grid=False, title='Number of births per year')

#Measuring the increase in naming diversity
table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex',yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))

