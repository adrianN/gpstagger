from datetime import datetime
from pytz import utc

def get_shot_time(jpeg, tz):
	""" Returns a datetime object containing the time the jpeg was created.
		We assume that the time has the format 'YYYY:MM:DD HH:MM:SS'
	"""
	#todo check the other time stamps in the exif data and think about which one to use
	time_str = jpeg.exif.primary.DateTime
	print "exif time", time_str, " in utc ", tz.localize(datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")).astimezone(utc)
	return tz.localize(datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")).astimezone(utc)

if __name__=="__main__":
	import pexif as pxf
	import sys
	img = pxf.JpegFile.fromFile(sys.argv[1])
	print get_shot_time(img)