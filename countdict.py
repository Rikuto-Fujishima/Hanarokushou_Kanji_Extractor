def countDict(outlist):
	countDict = dict()
	propDict = dict()
	for i in set(outlist):
		countDict[i] = outlist.count(i)
		propDict[i] = outlist.count(i) / len(outlist)
	return (countDict, propDict)
	
def combineDict(primaryCountDict, outlist):
	newList = []
	propDict = dict()
	countDict = dict()
	newCountDict = countDict(outlist)[1]
	for i, j in primaryCountDict.items():
		for k in range(0, j):
			newList.insert(0, i)
	for i in outlist:
		newList.insert(0, i)
	return countDict(newList)
	#countDict = {k:primaryCountDict.get(k,0) + newCountDict.get(k,0) for k in set(primaryCountDict | newCountDict)}