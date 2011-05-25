#!/usr/bin/env python

import urllib
from job import Job
from setup_menu import SetupMenu

class JobStatusParser:
    def __init__(self, base_uri, max_image_size, menu):
        self.base_uri = base_uri
        self.max_image_size = max_image_size
        self.menu = menu

    def parse(self, config):
        json_jobs = eval(urllib.urlopen(self.base_uri).read()).get("jobs")
        return json_jobs
