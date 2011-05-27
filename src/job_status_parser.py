#!/usr/bin/env python

import urllib
import logging
import json

class JobStatusParser:
    def __init__(self, base_uri, max_image_size):
        self.base_uri = base_uri
        self.max_image_size = max_image_size
        #        self.menu = menu

    def parse(self):
        raw_json = urllib.urlopen(self.base_uri).read()
        json_jobs = json.loads(raw_json).get("jobs")
        for job in json_jobs:
            logging.debug(job.get("name") + ", " + job.get("color"))
        return json_jobs
