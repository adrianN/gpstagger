import argparse
import re
import os
import sys
import tag

parser = argparse.ArgumentParser(description='Add GPS tags to some photos.')
parser.add_argument('gpx', help="A folder with gpx files.")
parser.add_argument('jpg', help="A folder with jpgs.")
parser.add_argument('-inplace',
	action="store_true",
	help="Modify pictures in place (default: store with _gps added to the filename)")

args = parser.parse_args()

gpx_dir = os.path.abspath(args.gpx)
jpg_dir = os.path.abspath(args.jpg)

jpeg_re = re.compile(".*\\.(jpg|jpeg)$", re.IGNORECASE)
gpx_re = re.compile(".*\\.gpx", re.IGNORECASE)

try:
	gpxfiles = [os.path.join(gpx_dir, f) for f in os.listdir(gpx_dir) if re.match(gpx_re, f)]
	jpegfiles = [os.path.join(jpg_dir, f) for f in os.listdir(jpg_dir) if re.match(jpeg_re, f)]
except OSError as e:
	print >> sys.stderr, "I can't open those directories\n\t", e
	exit(1)

print 'Reading files from', gpx_dir
print "\t"+'\n\t'.join(gpxfiles)
print 'Reading files from', jpg_dir
print "\t"+"\n\t".join(jpegfiles)

jpgs = tag.tag_all_photos(jpegfiles, gpxfiles)
for jpg in jpgs:
	jpg.writeFile(jpg.filename[:jpg.filename.rfind('.')]+'_gps.jpg')