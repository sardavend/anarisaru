from LogFile import LogFile
from FrameCalamp import FrameCalamp
#import re

class LogFileCalamp(LogFile):
	def __init__(self, fileName, format, ack):
		super(LogFileCalamp, self).__init__(fileName, format = 'f,m', ack = True)
		self.frames = []
		self.data = []
	
	def getFrames(self):
		for index,dat in enumerate(self.data):
			if(index % 2):
				self.frames.append(self.data[index].split(',')[0])
