import argparse
import re
import os
import sys
import tag
import pytz



def get_files(args):
	gpx_dir = os.path.abspath(args.gpx)
	jpg_dir = os.path.abspath(args.jpg)

	jpeg_re = re.compile(".*\\.(jpg|jpeg)$", re.IGNORECASE)
	gpx_re = re.compile(".*\\.gpx", re.IGNORECASE)

	gpxfiles = [os.path.join(gpx_dir, f) for f in os.listdir(gpx_dir) if re.match(gpx_re, f)]
	jpegfiles = [os.path.join(jpg_dir, f) for f in os.listdir(jpg_dir) if re.match(jpeg_re, f)]

	print 'Reading files from', gpx_dir
	print "\t"+'\n\t'.join(gpxfiles)
	print 'Reading files from', jpg_dir
	print "\t"+"\n\t".join(jpegfiles)

	return gpxfiles, jpegfiles

def get_args():
	parser = argparse.ArgumentParser(description='Add GPS tags to some photos.')
	parser.add_argument('gpx', help="A folder with gpx files.")
	parser.add_argument('jpg', help="A folder with jpgs.")
	parser.add_argument('-jpgtime', help="Timezone for the JPEG files. Understands all timezones\
		that pytz understands. (default=utc)")
	parser.add_argument('-gpxtime', help="Timezone for the GPX files. Understands all timezones\
		that pytz understands. (default=utc)")
	parser.add_argument('-inplace',
		action="store_true",
		help="Modify pictures in place (default: store with _gps added to the filename)")

	args = parser.parse_args()
	return args

def get_timezones(args):
	gpxtime = args.gpxtime if args.gpxtime else 'UTC'
	jpgtime = args.jpgtime if args.jpgtime else 'UTC'
	return pytz.timezone(gpxtime), pytz.timezone(jpgtime)

def lcs(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0 for j in xrange(n+1)] for i in xrange(m+1)]
    for i in xrange(1, m+1):
        for j in xrange(1, n+1):
            if X[i-1] == Y[j-1]:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C[m][n]

if __name__=="__main__":
	args = get_args()

	try:
		gpxfiles, jpegfiles = get_files(args)
	except OSError as e:
		print >> sys.stderr, "I can't open those directories\n\t", e
		exit(1)

	try:
		gpxtime, jpgtime = get_timezones(args)
	except LookupError as e:
		print "I don't understand the timezone", e.args[0]
		print "Did you mean", list(reversed(sorted(pytz.common_timezones, key=lambda s:lcs(e.args[0],s))[-3:])), "?"
		exit(1)


	jpgs = tag.tag_all_photos(jpegfiles, gpxfiles, jpgtime, gpxtime)
	for jpg in jpgs:
		if not args.inplace:
			jpg.writeFile(jpg.filename[:jpg.filename.rfind('.')]+'_gps.jpg')
		else:
			jpg.writeFile(jpg.filename)