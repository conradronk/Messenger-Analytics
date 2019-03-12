# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ijson 						# only needed for large files (not in mem), but the tutorial here called for it: https://www.dataquest.io/blog/python-json-tutorial/
import sys
from collections import defaultdict
from collections import Counter
# import scipy
# what else?

# Pull in a json file
try:
	file_name = "data/"+sys.argv[1]
except:
	print("data file not specficied or specified improperly. Reverting to \'data/message.json\'") ## TODO: Add a function to select the first json file in that directory, if it exists
	file_name = "data/message.json"
selected_attributes = [
	"sender_name",
	"content",
	"timestamp",
	"type"
]  # these are the attributes from the Facebook Messenger JSON format to pull

# <!----Defining all the needed functions----> (is that line thing from Java?)
def force(input_dict):
	new_dict = {
		"sender_name": "",
		"timestamp": 0,
		"content": "",
		"type": ""
	}
	new_dict["sender_name"] = input_dict["sender_name"]
	new_dict["timestamp"] = input_dict["timestamp"]
	new_dict["content"] = ""
	new_dict["type"] = input_dict["type"]
	return new_dict
	# function to force format, when content attribute is not present
	## TODO: Apparently this happens? Note when in the readme...

def sterilize_word(dirty):
	removables = [',', '.', '!', '?', ':', ';', '(', ')', '\"', '\'', '*']
	clean = False
	while not clean:
		if len(dirty) < 1:
			sterile_word = str(dirty)
			clean = True
		elif dirty[0] in removables:
			dirty = list(dirty)
			del dirty[0]
		elif dirty[-1] in removables:
			dirty = list(dirty)
			del dirty[-1]
		else:
			sterile_word = ''.join(dirty)
			clean = True
	return str(sterile_word)
	# Function to remove the unneeded leading characters. TODO: see if this might be where to remove links, etc.
	# Consider using re (a library, import re, for its .sub function, and also the built in .strip and .lower/.upper/.title functions
	# See page 72-73 for a neater way to process things in this way (lists of functions

def selectSubList(sender):
	subset = messages.loc[messages["sender_name"] == sender]
	list = []
	for line in subset.content:
		word_list = str(line).lower().split()
		list.extend(word_list)
	return list


# End Functions

with open(file_name, 'r') as f:
	objects = ijson.items(f, 'messages.item')
	rows = list(objects)
	#Consider re-writing or at least re-interpretting with the info on page 80 on in McKinney

#cleaning up the shitty ones, using the force function inline above
#Iterates through the "rows" dictionary, and if the content area is blank,
for column in rows:
	if column.get('content', 0) == 0:
			column = force(column)
	#else if column['type'] != 'generic': #for when there are multiple content keys
		#do stuff
		#not sure what this will be like down the line, but we'll see

messages = pd.DataFrame(rows, columns = ["sender_name", "timestamp", "content", "type"])

messages["date"] = pd.to_datetime(messages["timestamp"], unit="s")		#creates a new column, with the correctly formatted date

# print(messages["sender_name"].value_counts())

messages["indexed_content"] = messages.content.str.lower().str.split()


sender = input("Enter the name of the sender to query: ")
print(sender)

c = Counter(selectSubList(sender))
print(c.most_common(20))

#Getting word counts one way
word_counts = {}
for line in messages.content:
	word_list = str(line).lower().split()
	bare_word = ""
	for word in word_list:
		bare_word = sterilize_word(word)
		if bare_word in word_counts:
			word_counts[bare_word] += 1
		else:
			word_counts[bare_word] = 1

#print(word_counts)

#And a different way, using the Counter method from Collections
#Possibly more versatile? But needs to be passed a single list, which I guess could be used to select by certain attributes (i.e. count *where*...)

#What about list comprehensions? Page 67 in McKinney, basic form:
# expr for val in collection if condition
# x.lower() for x in strings if x.isdisjoint(forbidden)
#	Could I used set.isdisjoint, and some set of illegal characters? or stuff unique to the urls, photos, etc?
# can also produce a dict, or a set, or a list (see 67-68)

#To flatten a list of lists:
# flattened = [x for tup in some_tuples for x in tup] (A nested comprehension, page 69)


#use this unique function, in order to generate word counts
#NEED A NEW Dataframe that ust has all the words, and not all the messages
	#Might be able to iterate through each message, generate a list of uniques and then
