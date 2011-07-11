#!/usr/bin/env python

import urllib
import logging
import json

class JobStatusParser:
	def __init__(self, base_uri):
		self.base_uri = base_uri

	def parse(self):
		raw_json = urllib.urlopen(self.base_uri).read()
		json_jobs = json.loads(raw_json).get("jobs")
		return json_jobs
