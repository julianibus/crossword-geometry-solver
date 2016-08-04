
CLUEDB = "cluedb"
c = 0
with open(CLUEDB) as fileobject:
    for line in fileobject:
        print "line" + str(c)
        c = c+1
		
