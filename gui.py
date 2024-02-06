#reference
import os
import tkinter as tk
import pandas as pd
import openpyxl
from getkanji import *
from countdict import *
from getfile import *
from log import *
from tkinter import filedialog

#global variables
PRESENT = "花緑青◂Ⓘ▸"
lanSet = "English"
strin = ""
counter = dict()
prop = dict()
filePath = ""
fileName = ""
fileTarget = ""
outKanji = []
outCount = []
saveDefault = False
singleDefault = False

#global methods
def hideWidgetPack(widget):
    widget.pack_forget()
	
def hideWidgetPlace(widget):
    widget.place_forget()

def hideExtractor():
	hideWidgetPlace(lblPath)
	hideWidgetPlace(pathEntry)
	hideWidgetPlace(btnBrowse)
	hideWidgetPlace(btnStart)
	hideWidgetPlace(btnClear)
	hideWidgetPlace(btnSave)
	hideWidgetPlace(cbSave)
	hideWidgetPlace(cbExtract)
	hideWidgetPlace(lblInput)
	hideWidgetPlace(lblOutput)
	hideWidgetPlace(textInput)
	hideWidgetPlace(lbOutput)

#def hideCombiner():

def hideSettings():
	hideWidgetPlace(lblLan)
	hideWidgetPlace(btnEnglish)
	hideWidgetPlace(btnChinese)
	hideWidgetPlace(btnJapanese)
	hideWidgetPack(lblCopyright)
	hideWidgetPlace(lblLog)
	hideWidgetPlace(logTextb)
	
def extractorClick():
	#hideCombiner()
	hideSettings()
	lblPath.place(x=10, y=40, anchor="nw")
	pathEntry.place(x=10, y=80, height=30, anchor='nw')
	btnBrowse.place(x=710, y=80, anchor='ne')
	cbExtract.place(x=480, y=118)
	cbSave.place(x=480, y=142)
	btnStart.place(x=10, y=120, anchor='nw')
	btnClear.place(x=165, y=120, anchor='nw')
	btnSave.place(x=320, y=120, anchor='nw')
	lblInput.place(x=10, y=170, anchor="nw")
	lblOutput.place(x=550, y=170, anchor="ne")
	textInput.place(x=10, y=200, anchor="nw")
	lbOutput.place(x=710, y=200, anchor='ne')
	
def combinerClick():
	hideExtractor()
	hideSettings()
	
	
def settingsClick():
	hideExtractor()
	#hideCombiner()
	lblLan.place(x=10, y=40, anchor="nw")
	btnEnglish.place(x=10, y=80, anchor='nw')
	btnChinese.place(x=360, y=80, anchor='n')
	btnJapanese.place(x=710, y=80, anchor='ne')
	lblCopyright.pack(side='bottom')
	lblLog.place(x=10, y=120)
	logTextb.place(x=10, y=140)

def openFile():
	global pathEntry
	filePath = ""
	options = {
		'title': openFileTitle,
		'initialdir': '/',
		'filetypes': [('Supported Files', '*.txt *.lrc'), ('Text Files', '*.txt'), ('Lrc Files', '*.lrc'), ('All Files', '*.*')],
		'defaultextension': '*.txt *.lrc'
	}
	file = tk.filedialog.askopenfiles(mode='r', **options)
	if file is not None:
		for i in file:
			filePath += os.path.abspath(i.name)
			filePath += ';'
		filePath = filePath[:-1]
		if filePath != "":
			pathEntry.delete(0, tk.END)
			pathEntry.insert(0, filePath)
	else:
		print("No file!")

def extractCheck():
	global singleDefault
	if extractDefaultCheckbox.get() == 1:
		singleDefault = True
	else:
		singleDefault = False
	print(extractDefaultCheckbox)
	print(singleDefault)

def startExtracting():
	global pathEntry
	global filePath
	global strin
	global errorText
	global counter
	global prop
	global outKanji
	global outCount
	global textInput
	global lbOutput
	global singleDefault
	outKanji = []
	outCount = []
	FILETYPELIST = [".txt", ".TXT", ".txT", ".tXt", ".tXT", ".Txt", ".TxT", ".TXt", ".lrc", ".LRC", ".lrC", ".lRc", ".lRC", ".Lrc", ".LrC", ".LRc"]
	filePath = pathEntry.get().split(';')
	filePath = [x.strip() for x in filePath]
	print(filePath)
	strin = ""
	textInput.delete(1.0, tk.END)
	lbOutput.delete(0, tk.END)
	for files in filePath:
		if len(files) >= 4 and files[-4:] in FILETYPELIST:
			strin += getFile(files)
			textInput.insert(tk.END, strin)
		else:
			tk.messagebox.showerror(title='', message=errorText)
		strin += '\n'
	print(":::::::::::::::::::::::")
	print(singleDefault)
	if singleDefault == False:
		outlist = getKanji(strin)
	else:
		outlist = getSingleKanji(strin)
	print(outlist)
	counter = countDict(outlist)[0]
	print(counter)
	prop = countDict(outlist)[1]
	for i, j in counter.items():
		lbOutput.insert(tk.END, (i, j))
		outKanji.append(i)
		outCount.append(j)

def clearCache():
	global pathEntry
	global filePath
	global strin
	global counter
	global prop
	global textInput
	global lbOutput
	pathEntry.delete(0,tk.END)
	filePath = ""
	strin = ""
	counter = dict()
	prop = dict()
	textInput.delete(1.0, tk.END)
	lbOutput.delete(0, tk.END)

def defaultCheck():
	global saveDefault
	if saveDefaultCheckbox.get() == 1:
		saveDefault = True
	else:
		saveDefault = False
	print(saveDefaultCheckbox)
	print(saveDefault)

def saveFile():
	global saveDefault
	print(saveDefault)
	global filePath
	global fileName
	global fileTarget
	global outKanji
	global outCount
	global saveFileTitle
	contentList = filePath[0].split('\\')
	print(contentList)
	tempName = contentList[-1]
	tempNonName = []
	for i in contentList:
		tempNonName.append(i)
	tempNonName = list(reversed(tempNonName))
	tempNonName.pop()
	print(tempNonName)
	tempTarget = ""
	for i in tempNonName:
		tempTarget += i
		tempTarget += '\\'
	print(tempTarget)
	if outKanji != []:
		if saveDefault == True:
			fileName = tempName[:-4] + ".xlsx"
			fileTarget = tempTarget + fileName
			print(fileTarget)
			print(fileName)
		else:
			fileName = tempName[:-4] + ".xlsx"
			file = tk.filedialog.asksaveasfile(title=saveFileTitle, filetypes=[('Excel Files', '*.xlsx')], initialdir='/', initialfile=tempName[:-4]+'.xlsx')
			fileTarget = os.path.abspath(file.name)
			print(fileTarget)
		if fileName != "":
			data = {'Kanji': outKanji, 'Count': outCount}
			df = pd.DataFrame(data)
			df.to_excel(fileTarget, index=False)
			print("Saved.")
		else:
			print("No operations.")                      

def englishClick():
	setLan("English")
def chineseClick():
	setLan("中文")
def japaneseClick():
	setLan("日本語")
	
#main window initialize
mainWindow = tk.Tk()
mainWindow.geometry("720x400")
mainWindow.resizable(False, False)
mainWindow.title("Lyrics Kanji Extractor version 1.7")
mainWindow.iconbitmap("icon.ico")
#im = Image.open("icon.ico")
#img = ImageTk.PhotoImage(im)
#root.tk.call('wm', 'iconphoto', root._w, img)
extractDefaultCheckbox = tk.IntVar()
saveDefaultCheckbox = tk.IntVar()

#language initialize and set
lan = tk.StringVar()
lan.set("Language Setting:") #default
btnExtractorText = tk.StringVar()
btnExtractorText.set("Extractor") #default
btnCombinerText = tk.StringVar()
btnCombinerText.set("Combiner") #default
btnSettingsText = tk.StringVar()
btnSettingsText.set("Settings") #default
lblPathText = tk.StringVar()
lblPathText.set("TXT/LRC file path:") #default
openFileTitle = "Select File" #default
saveFileTitle = "Save as" #default
btnBrowseText = tk.StringVar()
btnBrowseText.set("Browse") #default
btnStartText = tk.StringVar()
btnStartText.set("Start Extracting") #default
btnClearText = tk.StringVar()
btnClearText.set("Clear Cache") #default
btnSaveText = tk.StringVar()
btnSaveText.set("Save File") #default
errorText = "File not selected or incorrect file type." #default
cbSaveText = tk.StringVar()
cbSaveText.set("Same name and path as source file") #default
cbExtractText = tk.StringVar()
cbExtractText.set("Extract single Kanji") #default
lblInputText = tk.StringVar()
lblInputText.set("Lyrics:") #default
lblOutputText = tk.StringVar()
lblOutputText.set("Results:") #default
logText = tk.StringVar()
logText.set("Update log") #default
updateLog = tk.StringVar()
updateLog.set(logEng) #default

def setLan(lanSet):
	global openFileTitle
	global errorText
	global saveFileTitle
	if lanSet == "English":
		mainWindow.title("Lyrics Kanji Extractor version 1.7")
		lan.set("Language Setting:")
		btnExtractorText.set("Extractor")
		btnCombinerText.set("Combiner")
		btnSettingsText.set("Settings")
		lblPathText.set("File path:")
		openFileTitle = "Select File"
		saveFileTitle = "Save as"
		btnBrowseText.set("Browse")
		btnStartText.set("Start Extracting")
		btnClearText.set("Clear Cache")
		btnSaveText.set("Save File")
		errorText = "File not selected or incorrect file type."
		cbSaveText.set("Same name and path as source file")
		cbExtractText.set("Extract single Kanji")
		lblInputText.set("Lyrics:")
		lblOutputText.set("Results:")
		logText.set("Update log")
		updateLog.set(logEng)
		logTextb.delete(1.0, tk.END)
		logTextb.insert(tk.END, logEng)

	elif lanSet == "中文":
		mainWindow.title("歌词汉字提取器 v1.7")
		lan.set("选择语言：")
		btnExtractorText.set("提取")
		btnCombinerText.set("合成")
		btnSettingsText.set("设置")
		lblPathText.set("TXT/LRC文件路径：")
		openFileTitle = "选择文件"
		saveFileTitle = "存储为"
		btnBrowseText.set("浏览")
		btnStartText.set("开始提取")
		btnClearText.set("清除缓存")
		btnSaveText.set("保存文件")
		errorText = "未选择文件或文件格式不正确。"
		cbSaveText.set("使用源文件相同路径和名称")
		cbExtractText.set("提取单字")
		lblInputText.set("歌词：")
		lblOutputText.set("结果：")
		logText.set("更新日志")
		updateLog.set(logChn)
		logTextb.delete(1.0, tk.END)
		logTextb.insert(tk.END, logChn)

	elif lanSet == "日本語":
		mainWindow.title("歌詞漢字イクストラクター ver 1.7")
		lan.set("言語を切り替え：")
		btnExtractorText.set("抽出")
		btnCombinerText.set("合成")
		btnSettingsText.set("設定")
		lblPathText.set("TXT/LRCファイルパス：")
		openFileTitle = "ファイルを選択"
		saveFileTitle = "保存先"
		btnBrowseText.set("参照")
		btnStartText.set("抽出開始")
		btnClearText.set("キャッシュをクリア")
		btnSaveText.set("ファイルを保存")
		cbExtractText.set("シングル漢字")
		errorText = "ファイルが選択されていません、または不正なファイル形式。"
		cbSaveText.set("ソースファイルと同じパスと名前")
		lblInputText.set("歌詞：")
		lblOutputText.set("結果：")
		logText.set("更新ログ")
		updateLog.set(logJpn)
		logTextb.delete(1.0, tk.END)
		logTextb.insert(tk.END, logJpn)

	else: #default
		mainWindow.title("Lyrics Kanji Extractor version 1.7")
		lan.set("Language Setting")
		btnExtractorText.set("Extractor")
		btnCombinerText.set("Combiner")
		btnSettingsText.set("Settings")
		lblPathText.set("File path:")
		openFileTitle = "Select File"
		saveFileTitle = "Save as"
		btnBrowseText.set("Browse")
		btnStartText.set("Start Extracting")
		btnClearText.set("Clear Cache")
		btnSaveText.set("Save File")
		errorText = "File not selected or incorrect file type."
		cbSaveText.set("Same name and path as source file")
		cbExtractText.set("Extract single Kanji")
		lblInputText.set("Lyrics:")
		lblOutputText.set("Results:")
		logText.set("Update log")
		updateLog.set(logEng)
		logTextb.delete(1.0, tk.END)
		logTextb.insert(tk.END, logEng)


#main window
btnExtractor = tk.Button(mainWindow, textvariable=btnExtractorText, width=32, height=1, command=extractorClick)
btnCombiner = tk.Button(mainWindow, textvariable=btnCombinerText, width=32, height=1, command=combinerClick)
btnSettings = tk.Button(mainWindow, textvariable=btnSettingsText, width=32, height=1, command=settingsClick)
btnExtractor.place(x=0, y=0, anchor='nw')
btnCombiner.place(x=360, y=0, anchor='n')
btnSettings.place(x=720, y=0, anchor='ne')

#Extractor
lblPath = tk.Label(mainWindow, textvariable=lblPathText, height=1)
pathEntry = tk.Entry(mainWindow, width=77)
btnBrowse = tk.Button(mainWindow, textvariable=btnBrowseText, width=20, height=1, command=openFile)
btnStart = tk.Button(mainWindow, textvariable=btnStartText, width=20, height=2, command=startExtracting)
btnClear = tk.Button(mainWindow, textvariable=btnClearText, width=20, height=2, command=clearCache)
btnSave = tk.Button(mainWindow, textvariable=btnSaveText, width=20, height=2, command=saveFile)
cbExtract =tk.Checkbutton(mainWindow, textvariable=cbExtractText, variable=extractDefaultCheckbox, onvalue=1, offvalue=0, command=extractCheck, height=1)
cbSave = tk.Checkbutton(mainWindow, textvariable=cbSaveText, variable=saveDefaultCheckbox, onvalue=1, offvalue=0, command=defaultCheck, height=1)
lblInput = tk.Label(mainWindow, textvariable=lblInputText, height=1)
lblOutput = tk.Label(mainWindow, textvariable=lblOutputText, height=1)
textInput = tk.Text(mainWindow, width = 65, height = 14)
lbOutput = tk.Listbox(mainWindow, width = 32, height = 10)

#Combiner
lblPathC = tk.Label(mainWindow, textvariable=lblPathText, height=1)
pathEntryC = tk.Entry(mainWindow, width=77)
btnBrowseC = tk.Button(mainWindow, textvariable=btnBrowseText, width=20, height=1, command=openFile)

#Settings
lblLan = tk.Label(mainWindow, textvariable=lan, height=1)
btnEnglish = tk.Button(mainWindow, text='English', width=28, height=1, command=englishClick)
btnChinese = tk.Button(mainWindow, text='中文', width=28, height=1, command=chineseClick)
btnJapanese = tk.Button(mainWindow, text='日本語', width=28, height=1, command=japaneseClick)
lblCopyright = tk.Label(mainWindow, text='Presented by Hanarokushou'+PRESENT[-3:], height=1)
lblLog = tk.Label(mainWindow, textvariable=logText, height=1)
logTextb = tk.Text(mainWindow, width = 99, height = 14)
logTextb.insert(tk.END, logEng)

#default


mainWindow.mainloop()