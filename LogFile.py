class LogFile(object):
    """Base LogFile Class needed to specializate all the Monnet Style Log,
    check Monnet's Developers Wiki to read more about """
	def __init__(self, fileName, format, ack = True):
		self.fileName = fileName 
		self.format= format 
		self.ack = ack 
		self.frames = []
		self.data = []

	def __removeEmptyLines(self,cleanLog):
		for index,line in enumerate(cleanLog):
			if(line == ''):
				cleanLog.pop(index)
		result = cleanLog
		return result 

	def cleanLog(self):
		with open(self.fileName) as f:
			readed = f.readlines()
			clean = [line.rstrip('\n\r') for line in readed]
			self.data = self.__removeEmptyLines(clean)
	
			








