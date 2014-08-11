#!/usr/bin/env python
# coding: utf8
import os
import os.path
import exifread
import database


def indexing(pathtoimage):
	imagepath = os.path.abspath(pathtoimage)
	if not os.path.exist(imagepath):
		return "Der Pfad %s existiert nicht" % imagepath
	foldername = os.path.dirname(imagepath)
	filename = os.path.basename(imagepath)
	f = open(imagepath, 'rb')
	try:
		tags = exifread.process_file(f, details=False)
	except:
		return "Irgendetwas beim Lesen der EXIF-Daten ging schief bei %s" % imagepath
	if tags == {}:
		return "File %s enthält keine EXIF-Daten" % imagepath
	f.close()
	# DateTime konvertieren von "yyyy:mm:dd hh:mm:ss" zu "yyyy-mm-dd hh:mm:ss"
	try:
		exif_datetimeoriginal = str(tags['EXIF DateTimeOriginal'])
		datetime = exif_datetimeoriginal[:4] + "-" + exif_datetimeoriginal[5:7] + "-" + exif_datetimeoriginal[8:]
	except:
		# EXIF-Daten enthalten kein "EXIF DateTimeOriginal"
		pass
	try:		
		imagemodel = str(tags['Image Model'])
		#TODO Kontrollen fehlen, Tags sind nicht einheitlich...
		query = "insert into test (name, path, datetime, imagemodel) values ('%s', '%s', TIMESTAMP '%s', '%s');" %(filename, foldername, datetime, imagemodel)
		status = database.write(query)
	except:
		logfile = open("/tmp/photoindexer.log", "a")
		logfile.writelines(pathtoimage + "\n")
		logfile.close()
		return
	return [foldername, filename, datetime, imagemodel, status]


# Ueber alle Files im photofolder loopen

def loopinfolder(photofolder):
	#logfile erstellen.
	logfile = open("/tmp/photoindexer.log", "a")
	logfile.write("Dies ist das Logfile\n")
	logfile.close()
	for root, dirs, files in os.walk(photofolder):
		for n in files:
			indexing(root + "/" + n)



