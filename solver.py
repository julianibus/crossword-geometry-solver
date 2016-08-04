#Crossword solving


import itertools
import random 
import time
import copy
import os
from datetime import *
DBDIR = "database"

# DEFINED FUNCTIONS

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def getcandidatesfromdb(p1, p2, l1, l2):
	letters = ['a', 'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	ldir1 = str(l1)
	ldir2 = str(l2)
	vwcandidates = list()
	hwcandidates = list()
	
	dlist1= list()
	dlist2= list()
	
	pairs = list()
	for ln in range(0,len(letters)):
		dlist1= list()
		dlist2= list()
		try:
			stream1 = open(DBDIR + "/" + ldir1 + "/" + str(p1) + letters[ln] + ".dat")
			tp1 = stream1.read().split("\n")
			tp1.pop()
			dlist1 = tp1
		except IOError:
			dummy = 0
		try:
			stream2 = open(DBDIR + "/" + ldir2 + "/" + str(p2) + letters[ln] + ".dat")
			tp2 = stream2.read().split("\n")
			tp2.pop()
			dlist2 = tp2
		except IOError:
			dummy = 0

		dl1 = len(dlist1)
		dl2 = len(dlist2)
		for i in range(0, len(dlist1)):
			for j in range(0, len(dlist2)):
				pairs.append(dlist1[i] + ";" + dlist2[j])
				dummy = 0
	
	return pairs	

print "Reading crossword puzzle..."
### I. Reading crossword ###
txt = open("crossword")

input = txt.read()

lines = input.split("\n")
chars = list()
for i in range(0,len(lines)):
	chars.append(list(lines[i]))
	
ysize = len(lines)
xsize = len(lines[0])

### II. Creating problem ###
#Look for words

wstartx = list()
wstarty = list()
wstartt = list()
wlen = list()
conds = list()

WALL = "-"
VERT = "2"
HORI = "1"
BOTH = "3"


for y in range(0,ysize - 1):
	for x in range(0,xsize - 1):
		field = chars[y][x]
		if field == VERT:
			wstartx.append(x)
			wstarty.append(y)
			wstartt.append(field)
			rx = x
			ry = y
			rfield = field
			while(rfield != WALL):
				ry = ry + 1
				rfield = chars[ry][rx]
			wlen.append(ry - y)
		elif field == HORI:
			wstartx.append(x)
			wstarty.append(y)
			wstartt.append(field)
			rx = x
			ry = y
			rfield = field
			while(rfield != WALL):
				rx = rx + 1
				rfield = chars[ry][rx]
			wlen.append(rx - x)
		elif field == BOTH:
			wstartx.append(x)
			wstarty.append(y)
			wstartt.append(VERT)
			wstartx.append(x)
			wstarty.append(y)
			wstartt.append(HORI)
			rx = x
			ry = y
			rfield = field
			while(rfield != WALL):
				ry = ry + 1
				rfield = chars[ry][rx]
			wlen.append(ry - y)
			rx = x
			ry = y
			rfield = field
			while(rfield != WALL):
				rx = rx + 1
				rfield = chars[ry][rx]
			wlen.append(rx - x)
			

### III. Finding conditions ###
wordscount = len(wstartx)

crossx = list()
crossy = list()
crossv = list()
crossh = list()
crossvi = list()
crosshi = list()

for y in range(0,ysize - 1):
	for x in range(0,xsize - 1):
		ind = list() #index
		indt = list()
		indvi = list()
		for w in range(0, wordscount):
			rx = wstartx[w]
			ry = wstarty[w]
			ro = wstartt[w]
			vi = 0
			for i in range(0,wlen[w]):
				if rx == x and ry == y:
					ind.append(w)
					indt.append(wstartt[w])
					indvi.append(vi)
				if wstartt[w] == VERT:
					ry = ry + 1
					vi = vi + 1
				elif wstartt[w] == HORI:
					rx = rx + 1
					vi = vi + 1
				
		if (len(ind) == 2):
			crossx.append(x)
			crossy.append(y)
			if (indt[0] == HORI):
				crossh.append(ind[0])
				crosshi.append(indvi[0])
				crossv.append(ind[1])
				crossvi.append(indvi[1])
			else:
				crossv.append(ind[0])
				crossvi.append(indvi[0])
				crossh.append(ind[1])
				crosshi.append(indvi[1])


### IV. Finding words with database ###
print "Gathering possible words..."
ncross = len(crossx)
wcandidates = list()
crosshcandidates = list()
crossvcandidates = list()
for i in range(0,ncross):
	l1 = wlen[crossh[i]]
	l2 = wlen[crossv[i]]
	
	p1 = crosshi[i]
	p2 = crossvi[i]
	
	# Reading db
	pairsraw = getcandidatesfromdb(p1,p2,l1,l2)
	pairs = pairsraw
	hwcandidates = list()
	vwcandidates = list()
	for p in range(0, len(pairs)):
		pair = pairs[p]
		ws = pair.split(";");
		hwcandidates.append(ws[0])
		vwcandidates.append(ws[1])
	crosshcandidates.append(hwcandidates)
	crossvcandidates.append(vwcandidates)


### V. Combining knowledge ###
print "Sorting out..."
	#crossx, crossy, crossh, crossv, crosshi, crossvi, crosshcandidates, crossvcandidates

maincandidates = list()

for h in range(0, wordscount):
	#print " word " + str(h) + "/" + str(wordscount)
	candidates = list()
	for g in range(0, ncross): 
		if crossh[g] == h: #horizontal word
			candidates.append(crosshcandidates[g])
			
		elif crossv[g] == h: #vertical word
			dummy = 0
			candidates.append(crossvcandidates[g])

	intersection = list(set.intersection(*map(set, candidates)))
	maincandidates.append(intersection)

#TWO METHODS:
#1.) CONTINUE ANALYSING DEPENDENDENCIES
#2.) PUT IN LETTERS AND CONTINUE SORTING OUT POSSIBILITIES

#nr 2


cmap = chars
print "Saving discoveries..."
#put in letters



def putinletters():
	for h in range(0, wordscount):
		if len(maincandidates[h]) == 1: #if the word has been determined distinctively
			solution = maincandidates[h][0]
			l = wlen[h]
			sx = wstartx[h]
			sy = wstarty[h]
			cx = sx
			cy = sy
			for f in range(0, l):
				cmap[cy][cx] = solution[f]
				if wstartt[h] == VERT:
					cy = cy + 1
				elif wstartt[h] == HORI:
					cx = cx + 1
					
putinletters()
print "Checking again..."
# last sortout based on letters put in


###########TEST

#maincandidates[8] = ['bye']
#maincandidates[16] = ['affe']
#maincandidates[3] = ['luftballon']
#maincandidates[0] = ['old']
###########

ATTEMPTS = 5
for at in range(0, ATTEMPTS):
	for h in range(0, wordscount):
		candidates = maincandidates[h]
		rcandidates = list()
		sx = wstartx[h]
		sy = wstarty[h]
		for c in range(0, len(candidates)):
			candidate = candidates[c]
			success = True
			for ln in range(0, wlen[h]):
				if wstartt[h] == VERT:
					if not cmap[sy + ln][sx] in [candidate[ln],VERT,HORI,BOTH,WALL,'0']:
						success = False
	
				elif wstartt[h] == HORI:
					if not (cmap[sy][sx + ln] in [candidate[ln],VERT,HORI,BOTH,WALL,'0']):
						success = False
			
			if success == True:
				rcandidates.append(candidate)
		maincandidates[h] = rcandidates # save changes
		#print rcandidates
	
	
	putinletters()

for h in range(0, wordscount): #clean maincandidates, remove duplicates	
	maincandidates[h] = list(set(maincandidates[h]))

### VI. Output the result ###
output = ""
for y in range(0,ysize -1 ):
	line = ""
	for x in range(0,xsize -1):
		line = line + cmap[y][x]
	output = output + line + "\n"
	
print output

for w in range(0, wordscount):
	print w, wstartx[w], wstarty[w], "-> ", len(maincandidates[w])	
	if len(maincandidates[w]) < 25: print maincandidates[w]
	if len(maincandidates[w]) == 0:
		print "\nNo solutions found."
		exit()

### VII. Backtracking algorithm (TRIAL AND ERROR) ##################################################
print "Finding solutions using backtracking algorithm..."				
SOLUTIONS = list()
maincandidates2 = copy.deepcopy(maincandidates)
cmap2 = copy.deepcopy(cmap)
maxwords = len(maincandidates2)


#define cross numbers of each word
crossnumbers = list()
for h in range(0, maxwords):
	sub = list()
	for g in range(0, ncross): 
		if crossh[g] == h or crossv[g] == h:
			sub.append(g)
	crossnumbers.append(sub)

print crossnumbers
#define crossing word numbers of each word
crossingwordnumbers = list()
for h in range(0, maxwords):
	sub = list()
	for g in range(0, len(crossnumbers[h])): 
		if crossh[crossnumbers[h][g]] == h:
			#sub.append([crossv[crossnumbers[h][g]],crossnumbers[h][g]])
			sub.append(crossv[crossnumbers[h][g]])
		elif crossv[crossnumbers[h][g]] == h:
			#sub.append([crossh[crossnumbers[h][g]],crossnumbers[h][g]])
			sub.append(crossh[crossnumbers[h][g]])
	crossingwordnumbers.append(sub)

print "crossingwordnumbers", crossingwordnumbers


#creating tree
#startwordnnr = 0
#usedwordnrs = list()
first = True

def findnextword(mcs, uw, cwordnr):
	choice = wordscount - 1 
	start = 10000000
	if choice != -1:
		for mc in range(0, len(mcs)):
		#	print choice, "before"
			if len(mcs[mc]) > 1:
				if first == False:
					if (len(mcs[mc]) < start and not (mc in uw) and mc != cwordnr and mc != cwordnr and mc in crossingwordnumbers[cwordnr]):
						choice = mc
						#print choice, (len(mcs[mc])), start
						start = len(mcs[choice])
				else:
					if (len(mcs[mc]) < start and not (mc in uw)):
						choice = mc
						#print choice, (len(mcs[mc])), start
						start = len(mcs[choice])
	return choice
		

maincandidateshist = list()
maincandidateshist = [maincandidates] * wordscount
cmaphist = list()
cmaphist = [cmap] * wordscount


SOLUTIONS = list()
solution = [""] * maxwords


usedwordnrs = list()
level = 0
#random.seed(datetime.now())
maincandidates2 = copy.deepcopy(maincandidates)
cmap2 = copy.deepcopy(cmap)
cwordnr = findnextword(maincandidates2, usedwordnrs, -1)

postoreach = len(maincandidates2[cwordnr])

first = False
cnr = 0

lastposition = [0] * wordscount

	
while (True):
	maincandidates2 = copy.deepcopy(maincandidateshist[level])
	cmap2 = copy.deepcopy(cmaphist[level])
	#crossingwordnrs = crossingwordnumbers[cwordnr]
	candidates = maincandidates2[cwordnr]
	maxcandidates = len(candidates)
	
	#cnr = random.randint(0,maxcandidates - 1)
	try: 
		candidate = candidates[cnr]
	except IndexError:
		# level up
		cwordnr = usedwordnrs[len(usedwordnrs) - 2]
		lastposition[level] = 0
		level = level - 1
		#usedwordnrs.pop() #######?????
		cnr = lastposition[level] + 1
		usedwordnrs.pop()
		if level == -1:
			break
			
		continue
		
	maincandidates2[cwordnr] = [candidate]
	solution[cwordnr] = candidate
	if len(usedwordnrs) > 0:
		if usedwordnrs[-1] != cwordnr:
			usedwordnrs.append(cwordnr)
	else:
		usedwordnrs.append(cwordnr)

    # put in letters
	for h in range(0, wordscount):
		if len(maincandidates2[h]) == 1: #if the word has been determined distinctively
			wsolution = maincandidates2[h][0]
			l = wlen[h] ############### THIS MIGHT BE WRONG ##########
			#l = len(wsolution)
		#	print wsolution," !! ", l
			sx = wstartx[h]
			sy = wstarty[h]
			cx = sx
			cy = sy
			for f in range(0, l):
				cmap2[cy][cx] = wsolution[f]
				if wstartt[h] == VERT:
					cy = cy + 1
				elif wstartt[h] == HORI:
					cx = cx + 1

		
	#check how many andidates are left
	solutionfailed = False
	for h in range(0, wordscount):
		wcandidates = maincandidates2[h]
		rcandidates = list()
		sx = wstartx[h]
		sy = wstarty[h]
		for c in range(0, len(wcandidates)):
			wcandidate = wcandidates[c]
			success = True
			for ln in range(0, wlen[h]):
				if wstartt[h] == VERT:
					if not cmap2[sy + ln][sx] in [wcandidate[ln],VERT,HORI,BOTH,WALL,'0']:
						success = False
	
				elif wstartt[h] == HORI:
					if not (cmap2[sy][sx + ln] in [wcandidate[ln],VERT,HORI,BOTH,WALL,'0']):
						success = False
		
			if success == True:
				rcandidates.append(wcandidate)
		
		maincandidates2[h] = rcandidates
		if len(rcandidates) == 0: # if somewhere no candidates are remaining the candidate chosen above must be wrong
			solutionfailed = True
	
	
	#cw = random.randint(0, len(crossingwordnrs) - 1
	cwnr = findnextword(maincandidates2, usedwordnrs, cwordnr) #find next word taken into account eventually
	#for w in range(0, wordscount):
	#	print w, wstartx[w], wstarty[w], "-> ", len(maincandidates2[w])	
		#if len(maincandidates2[w]) < 25: print maincandidates2[w]
	
	#OUTPUT
	cls()
	print "CROSSWORD PUZZLE SOLVER"
	print "pos.: \tlevel", level, "word", cwordnr	
	print "candidate: \t", candidate," (",cnr, "/", maxcandidates - 1,")"
	print "pos. matrix: \t", lastposition, postoreach
	print "solutions: \t", len(SOLUTIONS)
	print "words filled: \t", usedwordnrs
	print ""
	output = ""
	for y in range(0,ysize - 1):
		line = ""
		for x in range(0,xsize -1):
			line = line + cmap2[y][x]
		output = output + line + "\n"
	print output
	#crossnr = crossingwordnrs[cw][1]
	
	if solutionfailed == False:
		#print "works"
		if not cwnr in usedwordnrs:
		#	print cwordnr, "->", cwnr
			cwordnr = cwnr
			usedwordnrs.append(cwordnr)
			lastposition[level] = cnr
		#	print "cnr ", cnr
			level = level + 1
			cnr = lastposition[level] 
			maincandidateshist[level] = maincandidates2
			cmaphist[level] = cmap2
			cnr = 0
		else:
			if (cnr < maxcandidates - 1):
				cnr = cnr + 1
			else:
				#print cwordnr, "->", usedwordnrs[len(usedwordnrs) - 2]
				#print "in usedwords"
				#exit() ########################
				cwordnr = usedwordnrs[len(usedwordnrs) - 2]
			#	print cwordnr
				# level up
				lastposition[level] = 0
				level = level - 1
				usedwordnrs.pop()
				cnr = lastposition[level]   + 1
				#cnr = 0 ## THIS MIGHT BE WRONG
				
		#check if solution has been found
		merged = list(itertools.chain(*cmap2))
		if not HORI in merged and not VERT in merged and not '0' in merged:
			SOLUTIONS.append(solution)

	else:
		#print "failes"
		#cwordnr = usedwordnrs[len(usedwordnrs) - 2]
		if (cnr < maxcandidates - 1):
			#print "cnr erhoeht"
			cnr = cnr + 1
		else:
			# level up
			cwordnr = usedwordnrs[len(usedwordnrs) - 2]
			lastposition[level] = 0
			level = level - 1
			usedwordnrs.pop()
			cnr = lastposition[level]   + 1
			
			if level == -1:
				break
		#	print "cnrnew", cnr

		
print "Finished."

#print SOLUTIONS


