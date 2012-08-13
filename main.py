from CalampLogAnalizer import CalampLogAnalizer
from pykml.factory import KML_ElementMaker as KML
from lxml import etree
import sys
import time, datetime

def convertToKMl(message,icon):
	pm = KML.Placemark(
		KML.Style(
			KML.IconStyle(
				KML.scale(1.0),
				KML.Icon(
					KML.href(icon)
				),
			id="mystyle"		
			),
		id="pushpin"),
		KML.description('Movil ID: '+message.mId+'\n'+'OPERADOR: '+message.carrier+'\n'+'NIVEL RSSI: '+message.rssi+'\n'+'ESTADO DE COM.: '+message.commState),
		KML.styURL("pushpin"),
		KML.Point(KML.coordinates(message.longitude+','+message.latitude))
		)
	return pm

def __getFairCarrier(analizer):
	maximum = ''
	if(analizer.fairMessagePerCarrier['ENTEL'] > analizer.fairMessagePerCarrier['TIGO']):
		maximum = 'ENTEL'
	else:
		maximum = 'TIGO'
	return maximum





def app():
	if(sys.argv[1]!= ''):
		folder = KML.Folder()
		kmlFile = 'analisis'+str(int(time.time()))+'.kml'
		icon = ''
		placemarks = []
		analizador = CalampLogAnalizer(sys.argv[1])
		analizador.checkGSM()
		for index, message in enumerate(analizador.badMessages['fairMessages']):

			if(message.carrier == 'ENTEL'):
				icon = "http://maps.google.com/mapfiles/kml/paddle/red-diamond.png"
			elif(message.carrier == 'TIGO(TELECEL)'):
				icon = "http://maps.google.com/mapfiles/kml/paddle/blu-blank.png"
			if(message.carrier == 'VIVA(NUEVATEL)'):
				icon = "http://maps.google.com/mapfiles/kml/paddle/grn-blank.png"
			placemarks.append(convertToKMl(message,icon))
		[folder.append(place) for place in placemarks]
		
		for message in analizador.badMessages['noSignalMessages']:
			if(message.carrier == 'ENTEL'):
				icon = "http://maps.google.com/mapfiles/kml/paddle/red-diamond.png"
			elif(message.carrier == 'TIGO(TELECEL)'):
				icon = "http://maps.google.com/mapfiles/kml/paddle/blu-blank.png"
			if(message.carrier == 'VIVA(NUEVATEL)'):
				icon = "http://maps.google.com/mapfiles/kml/paddle/grn-blank.png"
			placemarks.append(convertToKMl(message,icon))
		[folder.append(place) for place in placemarks]

		#Write the kml file with all the placeMarks in the folder

		kmlFile = open(kmlFile,"a")
		kmlFile.write(etree.tostring(folder,pretty_print=True))
		print '============Resultados del Analisis============='
		print '- Se analizaron %d tramas' % analizador.numOfMessages
		print '- Ack perdidos: %d' % (analizador.numOfMessages - analizador.numOfAcks)
		print '- Cantidad de mensajes con senal pobre o sin senal: %d' % analizador.badMessages['num']
		print '- Cant. de Mensajes con senal Pobre: %d' % len(analizador.badMessages['fairMessages'])
		print '- Cant. de Mensajes Sin Senal: %d' % len(analizador.badMessages['noSignalMessages'])
		print '- El Operador que Presenta mas Problemas es %s' % __getFairCarrier(analizador)
		#print '- El rate de perdida por Operador es el siguiente:'
		#print '- ENTEL:%d 		TIGO:%d 		VIVA:%d' % (analizador.fairMessagePerCarrier['ENTEL'], analizador.fairMessagePerCarrier['TIGO'], analizador.fairMessagePerCarrier['VIVA'])
		print 'Si desea ver los datos en Google Earth, abra el  \narchivo analisis.kml en esta misma carpeta'
		print '================================================='
	else:
		print 'Usage: main.py [filename]'
if(__name__ == '__main__'): 
	app()





