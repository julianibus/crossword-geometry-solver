#Database creator
# -*- coding: utf-8 -*-

import os
import time
#/usr/share/dict/ogerman
db = open("words")
#db = open("newvok")
#db = open("/usr/share/dict/ogerman")
input = db.read()
words = input.split("\n")
wordscount = len(words)
maindir = "database"
if not os.path.exists(maindir):
	os.makedirs(maindir)
	
MAXLENGTH=10
counter = 0
for i in range(0,len(words) - 1):
	print str(i/float(wordscount) * 100) + "%"

	word = words[i]
	word = word.lower()
	print word
	if len(word) > MAXLENGTH:
		counter = counter + 1
		continue
	wordt = word.replace("ö","oe")
	word = wordt
	wordt = word.replace("ü","ue")
	word = wordt
	wordt = word.replace("ä","ae")
	word = wordt
	
	l = len(word)
	ldir = str(l)
	if (not os.path.exists(maindir + "/" + ldir)):
		os.makedirs(maindir + "/" + ldir)	
		
	for ln in range(0,len(word)):
		letter = word[ln]
		pos = ln
		fname = str(ln) + str(letter) + ".dat"
		with open(maindir + "/" + ldir + "/" + fname,"a+") as myfile:
			myfile.write(word + "\n")
	
print "100% - finished." + str(wordscount - counter) + " words. " + str(wordscount)
		


