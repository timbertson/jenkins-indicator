#!/usr/bin/env python

import urllib2
import logging
import json

class JobStatusParser:
	def __init__(self, base_uri):
		self.base_uri = base_uri
		proxy_support = urllib2.ProxyHandler({})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)

	def parse(self):
		response = urllib2.urlopen(self.base_uri)
		raw_json = response.read()
		json_jobs = json.loads(raw_json).get("jobs")
		return json_jobs
