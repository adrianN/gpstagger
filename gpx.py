import gpxpy
from bisect import bisect
import datetime as dt

class PositionLookup(object):
	def __init__(self, filenames):
		self._build_lookup(filenames)

	def _build_lookup(self, filenames):
		self.point_count = 0
		self.points = []
		for filename in filenames:
			with open(filename,'r') as gpxfile:
				gpx = gpxpy.parse(gpxfile)
				self.points.extend((p for p in gpx.walk(only_points=True) if p.time))
		self.points.sort(key=lambda p : p.time)
		self.point_count = len(self.points)
		self.times = [p.time for p in self.points]

	def lookup(self, time, time_cutoff=None):
		""" Returns the closest point to the given time. If the time difference is larger than
		    time_cutoff, return None.
		"""
		#do a binary search over the point set, comparing times
		pos = bisect(self.times, time)

		if pos > 0 and (time - self.times[pos-1]) < (self.times[pos]-time):
			#check which of the two adjacent times is closer to time
			return self.points[pos-1]
		return self.points[pos] if pos<self.point_count else self.points[pos-1]

if __name__ == "__main__":
	pos = PositionLookup(["./tests/track.gpx"])
	time = dt.datetime(2014, 3, 4, 13,1,9)
	for p in pos.points: print p
	print "closest point to", time
	print pos.lookup(time)