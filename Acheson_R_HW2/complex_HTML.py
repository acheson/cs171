#!/usr/bin/python
# Rob Acheson
# racheson@fas.harvard.edu
# 2/14/2013
# CS-171 HW2	


"""
#With the movie links, scrape each entry
#You will get the the following items:
#Produce a comma-separated text file (use semicolons to separate the entries) with a header row and the fields: 
#        Title of movie
#        Runtime
#        Genre (separated by semicolons if multiple)
#        Director(s)
#        Writer(s)
#        Actors (listed on the page directly only or first three, separated by semicolons)
#        Ratings
#        Number of Ratings


"""	
import csv, re, cStringIO, codecs

from pattern.web import abs as abs_url
from pattern.web import URL, DOM, plaintext, strip_between, cache, collapse_spaces
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT

#unicode writer
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            

# convenience methods
def clean_unicode(s):
	return s.encode('ascii', 'ignore')

# concatenate lists with ; between items
def concat_strings(list):
	str = ''
	for l in list[:-1]:
		str += l + "; "
	str += list[-1]
	return str	
	
# Creating the csv output file for writing into as well as defining the writer
output = open("complex_output.csv", "wb")
writer = UnicodeWriter(output)

# add header row
writer.writerow(["Movie Title", "Time", "Genre", "Directors", "Writers", "Actors", "Rating","Number of Ratings"])

# Get the DOM object to scrape for movie links. [Hint: Use absolute URL's.
# Documentation can be found here: http://www.clips.ua.ac.be/pages/pattern-web] 
url = URL("http://www.imdb.com/chart/top")
dom = DOM(url.download(cached=True))



#With the movie links, scrape each entry
#You will get the the following items:
#Produce a comma-separated text file (use semicolons to separate the entries) with a header row and the fields: 
#        Title of movie
#        Runtime
#        Genre (separated by semicolons if multiple)
#        Director(s)
#        Writer(s)
#        Actors (listed on the page directly only or first three, separated by semicolons)
#        Ratings
#        Number of Ratings


page_urls = []

tableRows = dom.by_id('main').by_tag('table')[1].by_tag('tr')
for tr in tableRows[1:]:
	a = tr.by_tag('a')[0]
	page_urls.append(clean_unicode(abs_url(a.attributes.get('href', ''), url.string)))

for p in page_urls:
	p_url = URL(p)
	p_dom = DOM(p_url.download(cached=True))
	
	title = clean_unicode(p_dom.by_class('header')[0].content)
	title = plaintext(strip_between('<span', '</span>', title))
	
	runtime = clean_unicode(p_dom.by_class('infobar')[0].by_tag('time')[0].content)

	genres = []
	for genre in p_dom.by_class('infobar')[0].by_tag('a')[:-1]:
		genres.append(clean_unicode(genre.content))
 	
 	directors = []
 	writers = []
 	actors = []

 	text_blocks = p_dom.by_class('txt-block')[:3]
 	for t in text_blocks:
 		spans = t.by_tag('span')
 		for s in spans:
 			if s.attributes.get('itemprop') == 'director':
				director = s.by_tag('span')[0].by_tag('a')[0].content
 				directors.append(clean_unicode(director))
 				
 			if s.attributes.get('itemprop') == 'writer':
				p_writer = s.by_tag('span')[0].by_tag('a')[0].content
 				writers.append(clean_unicode(p_writer))
 				
 			if s.attributes.get('itemprop') == 'actors':
				actor = s.by_tag('span')[0].by_tag('a')[0].content
 				actors.append(clean_unicode(actor))
 				
	rating = None
	ratings_count = None
 		
	spans = p_dom.by_class('star-box-details')[0].by_tag('span')
	for s in spans:
		if s.attributes.get('itemprop') == 'ratingValue':
			rating = clean_unicode(s.content)
		if s.attributes.get('itemprop') == 'ratingCount':
			ratings_count = clean_unicode(s.content)
			
	
	# format the strings from lists
	genres = concat_strings(genres)
	directors = concat_strings(directors)
	writers = concat_strings(writers)
	actors = concat_strings(actors)
	
	# add header row
 	writer.writerow([title, runtime, genres, directors, writers, actors, rating, ratings_count])
	
cache.clear()
output.close()














