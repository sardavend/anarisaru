from FrameCalamp import FrameCalamp
from LogFileCalamp import LogFileCalamp 
from LogAnalizer import LogAnalizer
import sys

class CalampLogAnalizer(LogAnalizer):
	def __init__(self, logFile):
		super(CalampLogAnalizer, self).__init__(logFile)
		self.numOfAcks = 0
		self.numOfMessages = 0
		self.fairMessagePerCarrier = {'ENTEL':0,'TIGO':0,'VIVA':0}
		self.badMessages ={'num': 0,'fairMessages':[], 'noSignalMessages':[]}
		self.messagesDecoded = []
		self.__initializer()


	def __initializer(self):
		try:
			if(sys.argv[1:]!= ''):
				self.logFile = LogFileCalamp(self.logFile,'d/message',True)
				self.logFile.cleanLog()
				self.logFile.getFrames()
				self.__decodeMessages()
				self.__countMessages()
			else:
				sys.stderr, 'usage: CalampLogFile.py [filename]'
		except IOError:
			print 'File Not Found'

	def __decodeMessages(self):
		for index, frame in enumerate(self.logFile.frames):
			message = FrameCalamp(frame)
			message.parseMessage('decoded')
			self.messagesDecoded.append(message)

	def __countMessages(self):
		for index, message in enumerate(self.logFile.frames):
			if(self.messagesDecoded[index].servicesType=='02'):
				self.numOfAcks += 1
			else:
				self.numOfMessages +=1

	def checkGSM(self):
		for index, message in enumerate(self.messagesDecoded):
			if(message.servicesType == '01'):
				if(message.rssi == 'Fair'):
					self.badMessages['num'] += 1
					self.badMessages['fairMessages'].append(self.messagesDecoded[index])
				if(message.rssi == 'No Signal'):
					self.badMessages['num'] += 1
					self.badMessages['noSignalMessages'].append(self.messagesDecoded[index])

		self.__getFairMessagePerCarrier()

	def __getFairMessagePerCarrier(self):

		for message in self.badMessages['fairMessages']:
			if(message.carrier == 'ENTEL'):
				self.fairMessagePerCarrier['ENTEL'] += 1
			if(message.carrier == 'TIGO(TELECEL)'):
				self.fairMessagePerCarrier['TIGO'] += 1
			if(message.carrier == 'VIVA(NUEVATEL)'):
				self.fairMessagePerCarrier['VIVA'] += 1

		for message in self.badMessages['noSignalMessages']:
			if(message.carrier == 'ENTEL'):
				self.fairMessagePerCarrier['ENTEL'] += 1
			if(message.carrier == 'TIGO(TELECEL)'):
				self.fairMessagePerCarrier['TIGO'] += 1
			if(message.carrier == 'VIVA(NUEVATEL)'):
				self.fairMessagePerCarrier['VIVA'] += 1






			










