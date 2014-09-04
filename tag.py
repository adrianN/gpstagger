from shottime import get_shot_time
from gpx import PositionLookup
from pexif import JpegFile
from pytz import utc
import sys

def gps_tag_photo(jpg, position_lookup, jpg_tz, time_cutoff=None):
	""" Adds gps information to the jpg using the position lookup structure.
	    Does not save the jpg, returns it instead """
	shot_time = get_shot_time(jpg, jpg_tz)
	print "Picture taken", shot_time
	position = position_lookup.lookup(shot_time, time_cutoff)
	print "position", position
	jpg.set_geo(position.latitude, position.longitude)

	return jpg

def tag_all_photos(jpg_filenames, gpx_filenames, jpg_tz=utc, gpx_tz=utc, time_cutoff=None):
	print "Parsing GPX data...",
	sys.stdout.flush()
	position_lookup = PositionLookup(gpx_filenames, gpx_tz)
	print "   ", position_lookup.point_count, "points read"
	jpegs = []
	for jpgname in jpg_filenames:
		print "Tagging", jpgname
		jpg = JpegFile.fromFile(jpgname)
		jpg = gps_tag_photo(jpg, position_lookup, jpg_tz, time_cutoff)
		jpegs.append(jpg)
	return jpegs
