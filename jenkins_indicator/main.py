#!/usr/bin/env python

import pygtk

pygtk.require('2.0')
import gtk
import gobject
import sys
import os
import logging
import ConfigParser
from job_status_parser import JobStatusParser
from config_dialog_builder import ConfigDialogBuilder
from job import Job
from job_images import JobImages
from indicator import Indicator
import subprocess

logging.basicConfig(level=logging.DEBUG)

from xdg import BaseDirectory

import yaml
class JenkinsApplet():
	timeout = 1000 * 10
	timeout_count = 1

	def __init__(self):
		self.indicator = Indicator(name="Jenkins", icon='unknown', description='Jenkins')
		self.update_status()
		gobject.timeout_add(self.update_interval, self.timer_callback)
	
	def init_config(self):
		self.config = self.load_config()
		config = self.load_config()
		connection_settings = config['connection']

		self.base_uri = connection_settings['base_uri']
		self.update_interval = int(connection_settings.get('update_interval', 5000))
		self.icons = JobImages(config['icons'])
		self.job_status_parser = JobStatusParser(self.base_uri)
	
	def load_config(self):
		try:
			filename = 'jenkins-indicator.yml'
			path = BaseDirectory.load_first_config(filename) or os.path.join(os.path.dirname(__file__), filename)
			logging.debug("loading config from: %s" % (path,))
			with open(path) as f:
				self._config = yaml.load(f)
				return self._config
		except StandardError, e:
			import traceback
			traceback.print_exc()
			if hasattr(self, '_config'):
				return self._config
			raise

	def item_callback(self, url):
		def cb():
			logging.debug("opening url: %s" % (url,))
			open_browser_command = ['/usr/bin/google-chrome', url]
			subprocess.call(open_browser_command)
		return cb

	def update_status(self):
		self.init_config()
		logging.debug("updating status")
		json_jobs = self.job_status_parser.parse()
		jobs = [Job(json_job, self.icons) for json_job in json_jobs]
		logging.debug("Jobs are: \n  " + "\n  ".join(map(repr, jobs)))

		self.indicator.clear()
		def important(job):
			globs = self.config.get('unimportant', [])
			from fnmatch import fnmatch
			for pattern in globs:
				if fnmatch(job.name, pattern):
					return False
			return True

		important_jobs = filter(important, jobs)
		unimportant_jobs = filter(lambda j: not important(j), jobs)

		def add_job(job):
			self.indicator.add_action(job.description(), self.item_callback(job.url))

		for job in important_jobs:
			add_job(job)
		self.indicator.add_action('less important:', None)
		for job in unimportant_jobs:
			add_job(job)

		self.indicator.add_action('--', None)
		self.indicator.add_action('Reload', self.update_status)
		self.indicator.add_action('Quit', self.quit)

		any_failed = any([not job.is_successful() for job in important_jobs])
		icon = self.icons['camellia_bad'] if any_failed else self.icons['camellia_good']
		self.indicator.set_icon(icon)
		  
		self.indicator.show()

	def quit(self):
		gtk.main_quit()

	def timer_callback(self):
		if self.timeout_count % (self.timeout / 1000) == 0:
			self.timeout_count = 0
			self.update_status()
		self.timeout_count += 1
		return True

if __name__ == '__main__':
	JenkinsApplet()
	gtk.main()
