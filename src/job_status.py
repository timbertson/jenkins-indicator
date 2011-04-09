#!/usr/bin/env python

import urllib

class JobStatus:
    base_uri = "http://localhost:8080/jenkins/api/python"

    def build(self):
        json_jobs = eval(urllib.urlopen(self.base_uri).read()).get("jobs")
        jobs = []
        for json_job in json_jobs:
            jobs.append(Job(json_job.get("name"), json_job.get("color")))
        return jobs

class Job:
    def __init__(self, name, color):
        self.name = name
        self.color = color

if __name__ == '__main__':
    parser = JobStatus()
    jobs = parser.build()
    for job in jobs:
        print("name: "+job.name+", "+job.color)
