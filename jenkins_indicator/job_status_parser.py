#!/usr/bin/env python

import urllib2
import logging
import json
import re
from BeautifulSoup import BeautifulSoup

class JobStatusParser:
	def __init__(self, base_uri):
		self.json_uri = base_uri + "/api/json"
		self.claims_uri = base_uri + "/claims/"
		proxy_support = urllib2.ProxyHandler({})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)

	def parse(self):
		response = urllib2.urlopen(self.json_uri)
		raw_json = response.read()
		json_jobs = json.loads(raw_json).get("jobs")
		self._add_claims(json_jobs)
		return json_jobs
	
	def _add_claims(self, jobs):
		#TODO: totally hacky - replace when claim plugin has a JSON API
		try:
			response = urllib2.urlopen(self.claims_uri)
			body = response.read()
			soup = BeautifulSoup(body)
			claim_rows = soup.find(id="projectStatus").findAll("tr")
			claims = {}
			for row in claim_rows:
				if row.find('th'):
					# ignore header row
					continue
				cells = row.findAll('td')
				logging.debug("cells=%r" % (cells,))
				(icon_cell, name_cell, date_cell, failure_duration_cell, status_cell, description_cell) = cells
				job_name = name_cell.find('a').text
				status = status_cell.text
				if status != 'unclaimed':
					logging.debug("status=%s" % (status,))
					claim_info = re.match('claimed by (?P<user>.*?) because: (?P<reason>.*)', status).groupdict()
					claims[job_name] = claim_info
			logging.debug("claimed jobs = %r" % (claims,))
		except StandardError, e:
			import traceback
			logging.warn("Couldn't process claims from %s\n%s" % (self.claims_uri, traceback.format_exc()))
			return

		for job in jobs:
			name = job['name']
			if name in claims:
				job['claimed'] = claims[name]

