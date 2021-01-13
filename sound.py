def getaudio(path, output = "output.mp3"):
	from os import system
	print("get sound...")
	system(f"ffmpeg -i {path} -acodec libmp3lame -loglevel quiet -metadata TITLE=\"from WM player\" {output}")

from threading import Thread
from playsound import playsound
from time import sleep

class Audio:
	def __init__(self, path):
		self.path = path
	def start(self):
		self.thread = Thread(target = self.play, args=())
		self.thread.start()
	def play(self):
		sleep(.1)
		playsound(self.path)