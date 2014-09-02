from shottime import get_shot_time
from gpx import PositionLookup
from pexif import JpegFile


def gps_tag_photo(jpg, position_lookup, time_cutoff=None):
	""" Adds gps information to the jpg using the position lookup structure.
	    Does not save the jpg, returns it instead """
	shot_time = get_shot_time(jpg)
	position = position_lookup.lookup(shot_time, time_cutoff)
	jpg.set_geo(position.latitude, position.longitude)
	return jpg

def tag_all_photos(photo_filenames, gpx_filenames, time_cutoff=None):
	position_lookup = PositionLookup(gpx_filenames)
	jpegs = []
	for jpgname in photo_filenames:
		jpg = JpegFile.fromFile(jpgname)
		jpg = gps_tag_photo(jpg, position_lookup, time_cutoff)
		jpegs.append(jpg)
	return jpegs
