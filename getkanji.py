import string
import re

def strip_punctuation(text):
	text = ''.join([c for c in text if c not in string.punctuation])
	chinese_punctuation = "！？｡＂＃＄％＆＇（）＊＋，。－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
	text = re.sub(r"[%s]+" % chinese_punctuation, "", text)
	return text

def strip_letter(text):
	ltr = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnmＱＷＥＲＴＹＵＩＯＰＡＳＤＦＧＨＪＫＬＺＸＣＶＢＮＭｑｗｅｒｔｙｕｉｏｐａｓｄｆｇｈｊｋｌｚｘｃｖｂｎｍ"
	text = re.sub(r"[%s]+" % ltr, "", text)
	return text

def isKanaTrans(strin):
	text = strip_punctuation(strin)
	print("====================")
	print(text)
	i = 1
	for j in range(0, len(text)):
		uc = hex(ord(text[j]))
		hx = int(uc, 16)
		if hx >= 0x3040 and hx <= 0x30ff:
			i += 1
			continue
		else:
			break
	if isKanaStr(text[:i - 1]) == True and isChinese(text[i:]) == True:
		return True
	else:
		return False

def isTrans(word):
	result = False
	transKanji = ["呐", "http", "//"]
	for i in word:
		if i in transKanji:
			result = True
			break
		else:
			continue
	return result

def isKanaStr(word):
	result = True
	for i in word:
		if isKana(i) == False:
			result = False
			break
		else:
			continue
	return result

def isChinese(word):
	result = True
	for i in word:
		uc = hex(ord(i))
		hx = int(uc, 16)
		if hx >= 0x4e00 and hx <= 0x9fff:
			continue
		else:
			result = False
			break
	return result

def sliceKanji(strin):
	strin = strip_punctuation(strin)
	strin = strip_letter(strin)
	strin = strin.replace(" ", "")
	strin = strin.replace("	", "")
	strin = strin.replace("　", "")
	result = []
	i = 0
	for j in range(0, len(strin)):
		if isKanji(strin[j]) == False:
			if j > i:
				result.append(strin[i:j])
			i = j + 1
	return result

def splitKanji(strin):
	outlist = []
	for i in range(0, len(strin)):
		strsrc = strin[i]
		uc = hex(ord(strsrc))
		hx = int(uc, 16)
		if hx >= 0x4e00 and hx <= 0x9fff:
			outlist.append(strsrc)
		else:
			continue
	return outlist

def isKana(ji):
	result = False
	uc = hex(ord(ji))
	hx = int(uc, 16)
	if hx >= 0x3040 and hx <= 0x30ff:
		if hx != 0x30fb:
			result = True
	return result

def isKanji(ji):
	result = False
	uc = hex(ord(ji))
	hx = int(uc, 16)
	if hx >= 0x4e00 and hx <= 0x9fff:
		result = True
	elif hx >= 0xff10 and hx <= 0xff19:
		result = True
	elif hx >= 0x0030 and hx <= 0x0039:
		result = True
	elif hx == 0x3005:
		result = True
	return result

def isPureKanji(ji):
	result = False
	uc = hex(ord(ji))
	hx = int(uc, 16)
	if hx >= 0x4e00 and hx <= 0x9fff:
		result = True
	elif hx == 0x3005:
		result = True
	return result

def isNum(ji):
	result = False
	uc = hex(ord(ji))
	hx = int(uc, 16)
	if hx >= 0xff10 and hx <= 0xff19:
		result = True
	elif hx >= 0x0030 and hx <= 0x0039:
		result = True
	return result

def isNumStr(strin):
	result = True
	for i in strin:
		if isNum(i) == True:
			continue
		else:
			result = False
			break
	return result

def isNihongo(word):
	result = False
	for i in word:
		if isKana(i) == True:
			result = True
	return result

def getSingleKanji(strin):
	outlist = []
	line = strin.split('\n')
	word = []
	for i in line:
		linelist = i.split('）')
		if len(linelist) > 1:
			if i[-1] != '）':
				linelist.pop()
			for j in linelist:
				pos = j.rfind("（")
				if pos >= 0:
					if pos + 1 < len(j):
						if isKana(j[pos + 1]) == True:
							word.append(j + '）')
		else:
			linelist = linelist[0].split(')')
			if len(linelist) > 1:
				if i[-1] != ')':
					linelist.pop()
				for j in linelist:
					j = j.replace('(', '（')
					pos = j.rfind("（")
					if pos >= 0:
						if pos + 1 < len(j):
							if isKana(j[pos + 1]) == True:
								word.append(j + '）')
			else:
				if isNihongo(linelist[0]) == True:
					if isTrans(linelist[0]) == False:
						if isKanaTrans(linelist[0]) == False:
							olist = sliceKanji(linelist[0])
							for k in olist:
								if len(k) < 5:
									word.append(k)
	for i in word:
		tempWord = i
		intI = i.rfind("（")
		intJ = len(i) - intI
		if isKana(tempWord[intI + 1]) == True: 
			for j in range(intJ + 1, len(i) + 1):
				strsrc = i[-j]
				if isKanji(strsrc):
					continue
				else:
					tempWord = i[-j + 1:]
					break
		if tempWord != '）':
			if tempWord[0] != '（':
				outlist.append(tempWord)
	removeList = []
	for i in outlist:
		stt = i[0]
		if "（" in i:
			if "）" in i:
				if i.rfind("）") - i.rfind("（") > 1:
					if isKana(i[i.rfind("（") + 1]) == False:
						removeList.append(i)
		elif stt == "{" or stt == "":
			removeList.append(i)
		elif isNumStr(i) == True:
			removeList.append(i)
	for i in removeList:
		outlist.remove(i)
	newOutList = []
	result = []
	for i in outlist:
		for j in i:
			if isKanji(j) == True:
				result.append(j)
	return result

def getKanji(strin):
	outlist = []
	line = strin.split('\n')
	word = []
	for i in line:
		i = i.replace(" ", "")
		i = i.replace("	", "")
		i = i.replace("　", "")		
		linelist = i.split('）')
		if len(linelist) > 1:
			if i[-1] != '）':
				linelist.pop()
			for j in linelist:
				pos = j.rfind("（")
				if pos >= 0:
					if pos + 1 < len(j):
						if isKana(j[pos + 1]) == True:
							word.append(j + '）')
		else:
			linelist = linelist[0].split(')')
			if len(linelist) > 1:
				if i[-1] != ')':
					linelist.pop()
				for j in linelist:
					j = j.replace('(', '（')
					pos = j.rfind("（")
					if pos >= 0:
						if pos + 1 < len(j):
							if isKana(j[pos + 1]) == True:
								word.append(j + '）')
			else:
				if isNihongo(linelist[0]) == True:
					if isTrans(linelist[0]) == False:
						if isKanaTrans(linelist[0]) == False:
							olist = sliceKanji(linelist[0])
							for k in olist:
								if len(k) < 5:
									word.append(k)
	for i in word:
		tempWord = i
		intI = i.rfind("（")
		intJ = len(i) - intI
		if isKana(tempWord[intI + 1]) == True: 
			for j in range(intJ + 1, len(i) + 1):
				strsrc = i[-j]
				if isKanji(strsrc):
					continue
				else:
					tempWord = i[-j + 1:]
					break
		if tempWord != '）':
			if tempWord[0] != '（':
				outlist.append(tempWord)
	removeList = []
	for i in outlist:
		stt = i[0]
		if "（" in i:
			if "）" in i:
				if i.rfind("）") - i.rfind("（") > 1:
					if isKana(i[i.rfind("（") + 1]) == False:
						removeList.append(i)
		elif stt == "{" or stt == "々":
			removeList.append(i)
		elif isNumStr(i) == True:
			removeList.append(i)
	for i in removeList:
		outlist.remove(i)
	return outlist