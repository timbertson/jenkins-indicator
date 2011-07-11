import logging
import gtk

class JobImages(object):
	def __init__(self, images):
		self.images = images

	def __getitem__(self, attr):
		return self.images.get(attr, 'unknown')

