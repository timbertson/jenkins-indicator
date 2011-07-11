import logging
import os

class JobImages(object):
	def __init__(self, images):
		self.images = images

	def __getitem__(self, attr):
		val = self.images.get(attr, None)
		if val is None:
			logging.debug("unknown image: %r" % (attr,))
			val = 'unknown'
		elif val.startswith('.'):
			val = os.path.abspath(os.path.join(os.path.dirname(__file__), val))
		logging.debug("image for %r = %s" % (attr, val))
		return val

