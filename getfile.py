def getFile(filePath):
	strin = ""
	f = open(filePath, "r", encoding='utf-8')
	line = f.readline()
	while line:
		strin += line
		line = f.readline()
	f.close()
	strin.encode(encoding='UTF-8',errors='strict')
	return strin