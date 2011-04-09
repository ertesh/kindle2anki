# This script gets all the highlights from kindle and saves in the file.
# It avoids saving the same content multiple times by keeping date of last sync. 

import os
import os.path
from datetime import datetime
from shutil import copyfile

KINDLE_DRIVE = "E:\\"
DEST = "notes.txt"
SYNCFILE = "sync.txt"
SEPARATOR = "=========="
DATE_FORMAT = "%A, %B %d, %Y, %I:%M %p" #Friday, January 28, 2011, 10:08 AM

def copy_notes():
	src = os.path.join(KINDLE_DRIVE, "documents", "My Clippings.txt")
	copyfile(src, DEST)
	
def get_last_sync():
	file = None
	try:
		file = open(SYNCFILE, "r")
		lastLine =  list(file)[-1].strip('-').strip()
		date = datetime.strptime(lastLine, DATE_FORMAT)
		return date
	except (IOError, IndexError):
		return datetime.min
	finally:
		if file is not None:
			file.close()

def parse(note):
	lines = note.strip().split("\n")
	book = lines[0]
	text = lines[-1]
	separatorPos = lines[1].find("|")
	tab = lines[1][:separatorPos].split(" ")
	type = tab[1]
	location = int(tab[3])
	dateStr = lines[1][11 + separatorPos:]
	try:
		date = datetime.strptime(dateStr, DATE_FORMAT)
	except Exception:
		print "Failed to parse", date
		date = datetime.now()
	return (book, type, location, date, text)
	
	
def read_file():
	f = open(DEST, "r")
	list = []
	note = ""
	for line in f:
		if line.find(SEPARATOR) < 0:
			note += line
		else:
			try:
				list.append(parse(note))
			except Exception:
				pass
			note = ""
	f.close()
	return list
	
def get_highlights(data, lastSync):
	for _, type, _, date, text in data:
		if type.find("Highlight") >= 0 and date >= lastSync:
			text = text.strip('.,!?\'\"')
			yield text

def sync(words):
	with open(SYNCFILE, "a") as myfile:
		
		for word in words:
			myfile.write(word + '\n')
		myfile.write("\n--- " + datetime.now().strftime(DATE_FORMAT) + "\n")
		

def clean():
	os.remove(DEST)

copy_notes()
lastSync = get_last_sync()
data = read_file()
words = get_highlights(data, lastSync)
sync(words)
clean()

