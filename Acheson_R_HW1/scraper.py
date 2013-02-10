"""
	Rob Acheson
	racheson@fas.harvard.edu

	2/7/2013
	
	CS-171 HW1	
	scraper.py
"""

# This is the introductory exercise to Pattern. We will try
# to guide you along as much as possible, but you should read
# up on documentation and get used to doing that. It's a really
# useful skill and a big part of programming is self-learning! 

# This is also just a skeleton
# so you actually don't have to use this at all. As long as your code 
# runs at the end of the day and produces the write results in a csv file, we're happy.

# Print is probably going to be your best friend for debugging so print often
# especially if something goes wrong.

#################################################################

# We are first importing from the pattern library and csv
import csv

from pattern.web import URL, DOM, plaintext, strip_between
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT

# Creating the csv output file for writing into as well as defining the writer
output = open("my_output.csv", "wb")
writer = csv.writer(output)

# Get the DOM object. Because this is the first exercise, we will only gather what's on this page.
# More complex example will come in HW2 with navigation of links 

url = URL("http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series")
dom = DOM(url.download(cached=True))
print("Retreiving Data...")

# At this stage in the process, you should look at the HTML source of this page
# You will get the the following items:
	# TV Title
	# Ranking
	# Genres (if any) separated by commas
	# Actors/actresses (if any) separated by commas
	# Runtime (if any) but you only keep the numbers

# There are many ways to go from here an you can really choose your own method

# To get you started, uncomment the following print line and see the output for the first entry

# print dom.by_class("title")[0].by_tag("a")[0].content

# by_class selects all with class="title" and returns a list. Familiarize yourself with the DOM
# by trying out different combinations. See what each returns.

# NOTE: if you see u' in front of your strings, you can use use encode( 'ascii', 'ignore' ) on your string
# to learn why, you can optionally read up on http://docs.python.org/2/howto/unicode.html 



##   	function to unescape HTML characters written by Fredrik Lundh
##		http://effbot.org/zone/re-sub.htm#unescape-html 

# fixes Monty Python's Flying Circus in output

import re, htmlentitydefs

# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
    
## End Fredrik Lundh code
 
 
 
def get_title(e):
	output = e.by_tag("a")[0].content
	output =unescape(output)
	
	return output.encode("ascii", "ignore")
	
# returns a formatted runtime for input element
def get_runtime(e):
	runtimes = e.by_class("runtime")
	if len(runtimes):
		runtime = e.by_class("runtime")[0].content
		# split the string to remove the " mins" - kinda had to use it after exercise.py
		return runtime.split()[0]
	else:
		return ""
		
# returns a ranking for input element
def get_ranking(e):	
	rankings = e.by_class("value")
	if len(rankings):
		return e.by_class("value")[0].content
	else:
		return ""	
		
# returns a string of genre(s) for input element
def get_genres(e):
	output = ""
	genres = e.by_class("genre")
	for g in genres:
		elements = g.by_tag("a")
		index = 0
		for e in elements:
			# concat the string
			output += e.content
		 	# if not on the last element, add comma and space
		 	if index < len(elements) - 1:
				output += ", "
				index += 1		
	return output.encode("ascii", "ignore")

# returns a string of actor(s) for input element
def get_actors(e):
	output = ""
	genres = e.by_class("credit")
	for g in genres:
		elements = g.by_tag("a")
		index = 0
		for e in elements:
			# concat the string
			output += e.content
		 	# if not on the last element, add comma and space
		 	if index < len(elements) - 1:
				output += ", "
				index += 1		
	return output.encode("ascii", "ignore")


# add header row
writer.writerow(["Title", "Ranking", "Genre", "Actors", "Runtime"])
allElements = dom.by_class("title")

for e in allElements:
	# parse the data
	title = get_title(e)
	ranking = get_ranking(e)
	genres = get_genres(e)
	actors = get_actors(e)
	runtime = get_runtime(e)
	# write to file
	writer.writerow([title, ranking, genres, actors, runtime])
	
# close the file	
output.close()

print("File saved as 'my_output.csv'")


# For your reference (taken from example in pattern-2.5)

# The DOM object is a tree of Element and Text objects.
# All objects inherit from Node, DOM also inherits from Element.

# Node.type          => NODE, TEXT, COMMENT, ELEMENT, DOM
# Node.parent        => Parent Node object.
# Node.children      => List of child Node objects.
# Node.next          => Next Node in Node.parent.children.
# Node.previous      => Previous Node in Node.parent.children.

# DOM.head      => Element with tag name "head".
# DOM.body      => Element with tag name "body".

# Element.tag        => Element tag name, e.g. "body".
# Element.attributes => Dictionary of tag attribute, e.g. {"class": "header"}
# Element.content    => Element HTML content as a string.
# Element.source     => Element tag + content

# Element.get_element_by_id(value)
# Element.get_elements_by_tagname(value)
# Element.get_elements_by_classname(value)
# Element.get_elements_by_attribute(name=value)

# You can also use short aliases: by_id(), by_tag(), by_class(), by_attribute()
# The tag name passed to Element.by_tag()
# can include a class ("div.message") or an id ("div#header").