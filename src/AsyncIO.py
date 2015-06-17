#-*- coding:utf-8 -*-

import threading
from Queue import Queue
import base64
import os
import time
import sys
import AsyncIO

def CreatFolder(Path):
	Pathstr=Path
	if Path.find('/')==-1:
		if not os.path.exists(Path):
			os.mkdir(Path)
	else:
		Path=Path.split('/')
		Path0=''
		for PathItem in Path:
			Path0=Path0+PathItem+'/'
			if not os.path.exists(Path0):
				os.mkdir(Path0)
	return Pathstr

def MakeBase64OutAsync(String,ImageFolder):
	Parts=String.split('}.dat')
	Base64=Parts[1]
	FileName=Parts[0].split(':')[-1]+'}.dat'
	FileHandle=open(CreatFolder(ImageFolder)+FileName,'wb')
	FileHandle.write(base64.b64decode(Base64))
	FileHandle.close()

class AsyncIO(threading.Thread):
	ToWrite=Queue()

	def __init__(self):
		threading.Thread.__init__(self)
		self.name='AsyncIO'

	def run(self):
		while True:
			Data=AsyncIO.ToWrite.get()
			MakeBase64OutAsync(Data[0],Data[1])

def PutOne(Data):
	AsyncIO.ToWrite.put(Data)

def init():
	App=AsyncIO()
	App.setDaemon(True)
	App.start()