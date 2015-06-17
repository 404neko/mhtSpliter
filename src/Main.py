#-*- coding:utf-8 -*-

import base64
import os
import time
import sys
import AsyncIO

def GetFileName(String):
	if String.find('/')==-1:
		if String.find('\\')==-1:
			return String
		else:
			String=String.split('\\')[-1]
			return String
	else:
		String=String.split('/')[-1]
		return String

def Log(String):
	print time.strftime('%I:%M:%S',time.localtime(time.time()))+' - '+String

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

def MakeImageFolder(FileName):
	FileName=GetFileName(FileName).split('.')[0]
	return 'Splited/'+FileName+'/Images/'

def MakeOutFolder(FileName):
	FileName=GetFileName(FileName).split('.')[0]
	return 'Splited/'+FileName+'/'

OutFolder='Splited/'
ImageFolder='Splited/Images/'
TrueImageFolder='Images/'
CreatFolder(ImageFolder)
MaxBuffer=1024

def MakeString(Num,Len):
	String=str(Num)
	while len(String)<Len:
		String='0'+String
	return String

def MakeBase64Out(String):
	Parts=String.split('}.dat')
	Base64=Parts[1]
	FileName=Parts[0].split(':')[-1]+'}.dat'
	FileHandle=open(CreatFolder(ImageFolder)+FileName,'wb')
	FileHandle.write(base64.b64decode(Base64))
	FileHandle.close()

def mthSplitInit(FileName):
	Log('Try to split .mth file...')
	FileHandle=open(FileName)
	FileHandle_Head=open(FileName+'_Head','wb')
	FileHandle_Message=open(FileName+'_Message','wb')
	FileHandle_Base64=open(FileName+'_Base64','wb')
	Count=0
	while True:
		Lines=FileHandle.readlines(MaxBuffer)
		if not Lines:
			break
		for Line in Lines:
			if Count==2:
				FileHandle_Base64.write(Line)
			else:
				if Line[0]=='-' and Line[1]=='-' and Line[2]=='-':
					Count+=1
					continue
				else:
					pass
				if Count==0:
					FileHandle_Head.write(Line)
				else:
					if Count==1:
						FileHandle_Message.write(Line)
					else:
						pass
	FileHandle.close()
	FileHandle_Head.close()
	FileHandle_Message.close()
	FileHandle_Base64.close()

def SplitMessage(FileName,MaxBlock):
	Log('Try to split message block file...')
	FileName=FileName+'_Message'
	FileHandle_Message=open(FileName)
	WriteCount=0
	FileCounter=0
	OutFileHandle=open(CreatFolder(OutFolder)+GetFileName(FileName).replace('.mht','')+'_Split_'+MakeString(FileCounter+1,3)+'.html','wb')
	OutFileHandle.write(
		'''<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>QQ Message</title><style type="text/css">body{font-size:12px; line-height:22px; margin:2px;}td{font-size:12px; line-height:22px;}</style></head><body><table width=100% cellspacing=0>'''
		)
	while True:
		Lines=FileHandle_Message.readlines(MaxBuffer)
		if not Lines:
			break
		for Line in Lines:
			if WriteCount<MaxBlock:
				OutFileHandle.write(Line.replace('IMG src="','IMG src="'+TrueImageFolder))
			else:
				OutFileHandle.close()
				FileCounter+=1
				OutFileHandle=open(CreatFolder(OutFolder)+GetFileName(FileName).replace('.mht','')+'_Split_'+MakeString(FileCounter+1,3)+'.html','wb')
				OutFileHandle.write(
					'''<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>QQ Message</title><style type="text/css">body{font-size:12px; line-height:22px; margin:2px;}td{font-size:12px; line-height:22px;}</style></head><body><table width=100% cellspacing=0>'''
					)
				WriteCount=0
				OutFileHandle.write(Line.replace('IMG src="','IMG src="'+TrueImageFolder))
			WriteCount+=1

def SplitBase64Block(FileName):
	Log('Try to make pictures out...')
	FileName=FileName+'_Base64'
	FileHandle_Base64=open(FileName)
	Buffer=''
	Count=0
	while True:
		Lines=FileHandle_Base64.readlines(MaxBuffer)
		if not Lines:
			break
		for Line in Lines:
			if Line[0]=='-' and Line[1]=='-' and Line[2]=='-' and Count!=0:
				MakeBase64Out(Buffer)
				Buffer=''
			else:
				Buffer=Buffer+Line
			Count+=1

def SplitBase64BlockAsync(FileName):
	Log('Try to make pictures out...')
	FileName=FileName+'_Base64'
	FileHandle_Base64=open(FileName)
	Buffer=''
	Count=0
	while True:
		Lines=FileHandle_Base64.readlines(MaxBuffer)
		if not Lines:
			break
		for Line in Lines:
			if Line[0]=='-' and Line[1]=='-' and Line[2]=='-' and Count!=0:
				AsyncIO.PutOne([Buffer,ImageFolder])
				Buffer=''
			else:
				Buffer=Buffer+Line
			Count+=1

def Now(FileName,MaxBlock):
	Log('Start running...')
	mthSplitInit(FileName)
	SplitMessage(FileName,MaxBlock)
	SplitBase64Block(FileName)
	Log('Cleaning...')
	os.removedirs('Splited/Images')
	Log('Success!')
	Path=os.path.abspath('.')+'\Splited'
	Command='explorer /select, "'+Path+'"'
	os.system(Command)

def NowAsync(FileName,MaxBlock):
	Log('Start running...')
	mthSplitInit(FileName)
	SplitMessage(FileName,MaxBlock)
	SplitBase64BlockAsync(FileName)
	Log('Cleaning...')
	os.removedirs('Splited/Images')
	Log('Success!')
	Path=os.path.abspath('.')+'\Splited'
	Command='explorer /select, "'+Path+'"'
	os.system(Command)

if __name__ == '__main__':
	AsyncIO.init()
	Log('This is mhtSpliter.')
	Log('Author: prprQueenSama@MoeMod')
	if len(sys.argv)==1:
		Log('Error: No parameter input.')
		raw_input()
	else:
		if len(sys.argv)==2:
			AimFile=sys.argv[1]
			ImageFolder=MakeImageFolder(AimFile)
			OutFolder=MakeOutFolder(AimFile)
			try:
				FileHandle=open('MaxBlock.txt')
				String=FileHandle.read()
				try:
					MaxBlock=int(String)
				except:
					MaxBlock=512
				FileHandle.close()
			except:
				MaxBlock=512
			NowAsync(AimFile,int(MaxBlock))
		else:
			if len(sys.argv)==3:
				AimFile=sys.argv[1]
				ImageFolder=MakeImageFolder(AimFile)
				OutFolder=MakeOutFolder(AimFile)
				MaxBlock=sys.argv[2]
				Now(AimFile,int(MaxBlock))
			else:
				Log('Error: Too many parameters input.')
				raw_input()