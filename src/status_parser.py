#!/usr/bin/env python

import urllib

class StatusParser:
    base_uri = "http://localhost:8080/jenkins/job/camellia/api/python"
    color = None

    def get_build_colour(self):
        self.build_status = eval(urllib.urlopen(self.base_uri).read())
        self.color = self.build_status.get("color")
        return self.color

if __name__ == '__main__':
    parser = StatusParser()
    parser.get_build_colour()
