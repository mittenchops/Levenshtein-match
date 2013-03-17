# pip install fuzzywuzzy
# pip install python-Levenshtein
import csv
from fuzzywuzzy import fuzz
from pprint import pprint
import Levenshtein
import numpy as np

threshold = 0.8
file1 = 'voters.csv'
file2 = 'donors.csv'

# Give me the first file
voters = []
with open(file1, 'r') as f:
	vals = csv.DictReader(f)
	for i in vals:
		voters.append(i)

# Give me the second file
donors = []
with open(file2, 'r') as f:
	vals = csv.DictReader(f)
	for i in vals:
		donors.append(i)

# for each donor, for each voter, compare their...
#	first name
#	last name
#	zip code
#	Then, return a value, matchval, that is the average of these three
#	matchval is defined on (0,1)
#	return a list() named "holder" that contains... 
#	a dict() "z" of the values, "d_id", "v_id", "firstname", "lastname"
holder = []
for x in donors:
	for y in voters:
#		z = dict(d_id = x['id'], v_id= y['id'], fmatch=Levenshtein.ratio(x["firstname"],y["firstname"]), lmatch=Levenshtein.ratio(x["lastname"],y["lastname"]), zmatch=Levenshtein.ratio(x["zip"],y["zip"]))
		matchval = np.mean([Levenshtein.ratio(x["firstname"],y["firstname"]),Levenshtein.ratio(x["lastname"],y["lastname"]),Levenshtein.ratio(x["zip"],y["zip"])])
		z = dict(d_id = x['id'], v_id= y['id'], matchval=matchval, match=(1 if matchval > threshold else 0))
		holder.append(z)

with open('out.csv', 'w') as csvoutput:
	wtr = csv.writer(csvoutput, dialect="excel")
	wtr.writerow(['d_id', "v_id", "match", "matchval"])
	for x in holder:
		wtr.writerow([x['d_id'],x['v_id'],x['match'],x['matchval']])
