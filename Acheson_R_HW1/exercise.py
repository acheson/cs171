"""
	Rob Acheson
	racheson@fas.harvard.edu

	2/7/2013
	
	CS-171 HW1	
	exercise.py
"""
# This is your first exercise in Python! Use it as
# a warmup exercise. 

# The built-in aString.split() in Python only uses
# whitespace to split the string. This is annoying because
# if you had a sentence with punctuation marks,
# the procedure won't be able to recognize it.

# Define a procedure, split_string, that takes two
# inputs: the string to split and a string containing
# all of the characters considered separators. The
# procedure should return a list of strings that break
# the source string up by the characters in the
# splitlist.

# We have started this for you. Fill in the blanks.
# Python is a whitespace language so be careful with
# your indents.

# Source is your long text string that needs separation
# Separators is a string containing all the symbols you
# want as separators 

# DO NOT USE split() but you can import other libraries (i.e. regular expressions)

# There are many solutions so as long as it works! 


def split_string(source, separators): 

	# create an empty list
	out = []
	
	#keep track of where to start slicing the string
	start = 0
	
	# iteration based on the example
	# http://docs.python.org/2/tutorial/controlflow.html#for-statements
	for i in range(len(source)):
		
		# compare each char to the separators
		for s in separators:
			
			# if a separator was found slice out a word and push it on out list
			if source[i] == s:
				
				word = source[start:i]
				
				# in case of redundant separators, check that word has chars
				if len(word) > 0:
					out.append(word)
					word = ""
					
				# update the starting index
				start = i + 1
		
		
	# in the event the last char is not a separator this will add the last one
	word = source[start:len(source)]
	if word != "":
		out.append(word)
		
	return out


# To test, uncomment these:

out = split_string("Before  the rain   ...  there was lightning and thunder.", " .")
print out
#>>> ['Before', 'the', 'rain', 'there', 'was', 'lightning', 'and', 'thunder']