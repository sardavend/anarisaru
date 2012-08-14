from Trama import Frame

class FrameCalamp(Frame):
    """This class define all the fundation of a message encoding in LMUDirect
    app protocol"""
	def __init__(self,trama):
		super(FrameCalamp,self).__init__(trama)
		self.option = ''
		self.mIdLength = ''
		self.mId = ''
		self.mIdTypeLength = ''
		self.mIdType = ''
		self.servicesType = ''
		self.messageType = ''
		self.sequence = ''
		self.updateTime = ''
		self.updateFix = ''
		self.latitude = ''
		self.longitude = ''
		self.altitude = ''
		self.speed = ''
		self.heading = ''
		self.satellites = ''
		self.fixStatus = ''
		self.carrier = ''
		self.rssi = ''
		self.commState = ''
		self.hdop = ''
		self.inputs = ''
		self.unitStatus = ''
		self.eventIndex = ''
		self.eventCode = ''
		self.accum = ''
		#fields for ACK type
		self.type = ''
		self.ack = ''
		self.appVersion = ''

	
	def parseMessage(self,option = 'hex'):

		if(option=='hex'):
			self.option = self.trama[0:2] # 1 byte
			self.mIdLength = self.trama[2:4] # 1 byte
			length = self.__getLength(self.mIdLength) #get movil id length
			self.mId = self.trama[4:length] # variable bytes, default 5 bytes
			self.mIdTypeLength = self.trama[length:length+2] # 1 byte
			self.mIdType = self.trama[length+2:length+4] # 1 byte
			self.servicesType = self.trama[length+4:length+6] # 1 byte
			#check if the message is Ack type
			if(self.servicesType == '02'):
				self.messageType = self.trama[length+6:length+8] # 1 byte
				self.sequence = self.trama[length+8:length+12] # 2 bytes
				self.type = self.trama[length+12:length+14] # 1 byte
				self.ack = self.trama[length+14:length+16] # 1 byte
				self.appVersion = self.trama[length+16:length+22] # 3 bytes
				return
			self.messageType = self.trama[length+6:length+8] # 1 byte
			self.sequence = self.trama[length+8:length+12] # 2 bytes
			self.updateTime = self.trama[length+12:length+20] # 4 bytes
			self.updateFix = self.trama[length+20:length+28] # 4 bytes
			self.latitude = self.trama[length+28:length+36] # 4 bytes
			self.longitude = self.trama[length+36:length+44] # 4 bytes
			self.altitude = self.trama[length+44:length+52] # 4 bytes
			self.speed = self.trama[length+52:length+60] # 4 bytes
			self.heading = self.trama[length+60:length+64] # 2 bytes
			self.satellites = self.trama[length+64:length+66] # 1 byte
			self.fixStatus = self.trama[length+66:length+68] # 1 byte
			self.carrier = self.trama[length+68:length+72] # 2 bytes
			self.rssi = self.trama[length+72:length+76] # 2 bytes
			self.commState = self.trama[length+76:length+78] # 1 byte
			self.hdop = self.trama[length+78:length+80] # 1 byte
			self.inputs = self.trama[length+80:length+82] # 1 byte
			self.unitStatus = self.trama[length+82:length+84] # 1 byte
			self.eventIndex = self.trama[length+84:length+86] # 1 byte
			self.eventCode = self.trama[length+86:length+88] # 1 byte
			self.accum = self.trama[length+88:length+90] # 1 byte
		elif(option == 'decoded'):
			self.parseMessage()
			self.__decodePosition()
			self.__decodeWireless()
		else:
			print 'Invalid Option, Try : hex or decoded'

						
	def __getLength(self,length):
		length = 4 + int(length) * 2
		return length

	def __parseTwoComplements(self, hexNumber):
		try:
			intNumber = int(bin(int('0x'+ hexNumber, 16)), 2)-(1<<len(hexNumber)/2*8)+1
			return intNumber
		except:
			pass

	def __decodeWireless(self):
		'''refer to MNC on http://en.wikipedia.org/wiki/Mobil_Network_Code#B
			carrier 01 nuevatel(viva)
			carrier 02 Entel
			carrier 03 Telecel(Tigo)
			-112 No Signal
			-80 Fair
			-78 good
			-76 good
			-72 good
			-70 good
			-66 very good
			-60 very good
			-58 very good '''
		#Decode RSSI
		rssiDecoded = self.__parseTwoComplements(self.rssi)
		if(rssiDecoded >= -68 ): 
			self.rssi = 'Very Good'
		if(rssiDecoded >= -78 and rssiDecoded <= -70):
			self.rssi = 'Good'
		if(rssiDecoded <= -80 and rssiDecoded >= -100):
			self.rssi = 'Fair'
		if(rssiDecoded <= -110):
			self.rssi = 'No Signal'
		#Decode CommState
		commStates = ['Avail','Network','Data','Connected','VoiceCallActive','Roaming', 'NotConnected']
		validCommStates = []
		try:
			commStateDecoded = int('0x' + self.commState, 16)
			bits = bin(commStateDecoded)[2:]
			indexs = len(bits)-1
			stateIndex = 0
			while(indexs):
				if(bits[indexs] == '1'):
					validCommStates.append(commStates[stateIndex])
				indexs -= 1
				stateIndex += 1
	
			if(validCommStates == []):
				self.commState = commStates[-1]
			else:
				self.commState = ",".join(validCommStates)
		except:
			pass
		

		#check Carrier
		if(self.carrier == '0002'):
			self.carrier = 'ENTEL'
		elif(self.carrier == '0003'):
			self.carrier = 'TIGO(TELECEL)'
		if(self.carrier == '0001'):
			self.carrier = 'VIVA(NUEVATEL)'

	def __decodePosition(self):
		tmpLatitude=[]
		tmpLongitude=[]
		lat = str(self.__parseTwoComplements(self.latitude))
		tmpLatitude.append(lat[0:3])
		tmpLatitude.append(lat[3:-1])
		lon = str(self.__parseTwoComplements(self.longitude))
		tmpLongitude.append(lon[0:3])
		tmpLongitude.append(lon[3:-1])
		self.latitude = '.'.join(tmpLatitude)
		self.longitude = '.'.join(tmpLongitude)








		

		
		

		



