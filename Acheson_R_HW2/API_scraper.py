#!/usr/bin/python
# Rob Acheson
# racheson@fas.harvard.edu
# 2/14/2013
# CS-171 HW2	

# Welcome to Twitter data exercise! 
# To help you get started, you should look at the 03-twitter.py example that comes with pattern-2.5.
# Much of the code is written there for you. You just have to understand it!

# INSTRUCTIONS

# 1) Using Pattern stream API for Twitter, write output to twitter_output.csv
# 2) Search for 100 tweets with "visualization" in them 
# 3) Make sure they are unique (HINT: look at 03-twitter.py and the example with index)
# 4) Each row should have:
		# 	Author_of_tweet		
		#   Date (in format of 01/25/2013)
		#	Time (in format of 00:25:29)	
		#	Text_of_tweet (as a string)	
		#	Hashtag1 (if any) with first hashtag word without hashtag symbol in front of it
		#	Hashtag2 (if ang)
		#	...
		
# Output should be in the same style as the following 

	#		christina98		01/25/2013		00:24:59	visualization rocks! #viz #visual #fun			viz		visual		fun
	#		spencer88		01/25/2013		00:25:29	visualization of food. #food					food
	#		george100		01/25/2013		00:23:27	d3.js visualization	struggz			
	
# 5) Make sure we can read your code!

### much of this code is based on the example03-twitter.py from Pattern.Web ###

import os, sys; sys.path.insert(0, os.path.join("..", ".."))
import datetime, time

from pattern.web import Twitter, hashtags
from pattern.db  import Datasheet, pprint


# concatenate lists with , between items
def concat_strings(list):
	str = ''
	# add comma to all but last item
	for l in list[:-1]:
		#remove the first character from l (the hashtag symbol)
		str += l[1:] + ", "
	#  always return the last item (could be the only), remove the first caracter here as well	
	str += list[-1][1:]
	return str	

# This example retrieves tweets containing given keywords from Twitter (http://twitter.com).
try: 
    # We store tweets in a Datasheet that can be saved as a text file (comma-separated).
    # In the first column, we'll store a unique ID for each tweet.
    # We only want to add the latest tweets, i.e., those we haven't previously encountered.
    # With an index on the first column we can quickly check if an ID already exists.
    # The index becomes important once more and more rows are added to the table (speed).
    table = Datasheet.load("twitter_output.csv")
    index = dict.fromkeys(table.columns[0], True)
except:
    table = Datasheet()
    index = {}
    # first run - add header row to table
    table.append(['ID', 'AUTHOR', 'DATE', 'TIME(GMT)', 'TWEET', 'HASHTAGS'])
    

engine = Twitter(language="en")

# With cached=False, a live request is sent to Twitter,
# so we get the latest results for the query instead of those in the local cache.
for tweet in engine.search("visualization", count=100, cached=False):
    print tweet.text
    print tweet.author
    print tweet.date
    print hashtags(tweet.text)

    # Create a unique ID based on the tweet content and author.
    id = str(hash(tweet.author + tweet.text))

    author = tweet.author
    dt = datetime.datetime.strptime(tweet.date, "%a, %d %b %Y %H:%M:%S +0000")
    date = dt.strftime("%m/%d/%Y")
    time = dt.strftime("%H:%M:%S")
    hashes = hashtags(tweet.text)
    if len(hashes) > 0:
    	hashes = concat_strings(hashes)
    else:
    	hashes = None

    # Only add the tweet to the table if it doesn't already contain this ID.
    if len(table) == 0 or id not in index:
        
        table.append([id, author, date, time, tweet.text, hashes])
        # table.append([id, tweet.text])
        index[id] = True

table.save("twitter_output.csv")

print "Total results:", len(table)
print
