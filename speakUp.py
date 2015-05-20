#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gtts import gTTS

import sys
import os
import re
import shutil
import time
import subprocess
from datetime import datetime



#for a very big database ;)
import sqlite3

#to treat cgi requests:
import cgi, cgitb

import argparse

class SpeakUp:
	"""gTTS (google text-to-speak) wrapper via command-line and CGI interface
		Each translated word or sentence is saved, allowing it to be played in
		the future just in case the network is down and we cannot reach
		google servers.
	"""
	currentPath = os.path.dirname(os.path.abspath(__file__))
	audioDir = os.path.join(currentPath, "mp3")
	db = os.path.join(currentPath, "index.db")

	audioPlayer = "mplayer"
	audioProc = None
	dbConn = None
	debugMode = False

	def __init__(self, debugMode = False):
		self.debugMode = debugMode

		if (os.path.exists(self.db)):
			self.openDatabase()
		else:
			self.createDatabase()
			self.openDatabase()

	def createDatabase(self):
		self.debug("creating database")
		try:
			if (os.path.exists(self.audioDir)):
				shutil.rmtree(self.audioDir)

			os.makedirs(self.audioDir)

			self.dbConn = sqlite3.connect(self.db)
			cur = self.dbConn.cursor()
			sql = "CREATE TABLE mp3 (message TEXT, language TEXT, filepath TEXT, creation DATE);"

			self.debug(sql)

			cur.executescript(sql)
			self.dbConn.commit()

		except sqlite3.Error, e:
			print(e)
			self.dbConn.rollback()
			sys.exit(1)

		finally:
			if self.dbConn:
				self.closeDatabase()

	def openDatabase(self):
		self.debug("opening database: {}".format(self.db))
		self.dbConn = sqlite3.connect(self.db)
		self.dbConn.text_factory = str

	def closeDatabase(self):
		self.debug("closing database")
		self.dbConn.close()

	def say(self, text, lang='en'):
		self.debug("locating '{}' to play".format(text))
		cur = self.dbConn.cursor()
		sql = "SELECT * FROM mp3 WHERE message LIKE '{}' AND language LIKE '{}';".format(text, lang)

		self.debug(sql)

		cur.execute(sql)
		row = cur.fetchone()
		if row == None:
			self.appendText(text, lang)
			self.say(text, lang)
		else:
			self.play(str(row[2])) # 0=message 1=language 2=filepath 3=creation

	def play(self, filepath):
		self.debug("playing {}".format(filepath))
		self.debug("\n")

		FNULL = open(os.devnull, 'w')
		self.audioProc = subprocess.call([self.audioPlayer, filepath], stdout=FNULL, stderr=subprocess.STDOUT)
		#self.mp3_player_proc = subprocess.Popen([self.mp3_player, file_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#stop playing with: player.stdin.write("q")

	def appendText(self, txt, language):
		self.debug("appending to db: '{}'".format(txt))

		tts = gTTS(text=txt, lang=language)
		name = re.sub('[^0-9a-zA-Z]+', '_', txt)
		timeStr = str(int(time.time()))
		output = name + "_" + timeStr + ".mp3"
		output = os.path.join(self.audioDir, output)

		self.debug("saving to: '{}'".format(output))

		tts.save(output)
		now = datetime.now()
		con = self.dbConn.cursor()
		sql = "INSERT INTO mp3(message, language, filepath, creation) VALUES('{}', '{}', '{}', '{}')".format(txt, language, output, now)

		self.debug(sql)

		con.execute(sql)
		self.dbConn.commit()

	def debug(self, s):
		if self.debugMode:
			print(s)



if __name__ == "__main__":
	s = SpeakUp(debugMode=False)

	#was a request from web?
	form = cgi.FieldStorage()
	msg = form.getvalue('msg')
	if msg == None:
		#if not, user must provide the text to speak
		parser = argparse.ArgumentParser(description='Command line  and CGI interface to gTTS')
		parser.add_argument('-m','--msg', help="Text to speak", nargs='?', required=True)
		parser.add_argument('-v','--verbose', help="Debugging mode", nargs='?', required=False)

		args = parser.parse_args()

		# if user provided a message
		if args.msg == None:
			print("No message provided...")
		else:
			s.say(str(args.msg))

	else:
		print (	"Content-type:text/html\r\n\r\n\
				<html>\
					<head><title>speakUp</title></head>\
					<body> <h2>Message: {}</h2> </body>\
				</html>".format(msg))
		s.say(msg)
