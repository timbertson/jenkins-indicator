#!/usr/bin/env python

import pygtk

pygtk.require('2.0')
import gtk
import gobject
import sys
import logging
import ConfigParser
from job_status_parser import JobStatusParser
from job import Job
from indicator import Indicator
import subprocess

logging.basicConfig(level=logging.DEBUG)

#TODO: xdg for app.properties

class JenkinsApplet():
    timeout = 1000 * 10
    timeout_count = 1
    icon_error = 'empathy-busy'
    icon_success = 'empathy-available'


    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("app.properties")
        self.base_uri = self.config.get('connection_settings', 'base_uri')
        self.update_interval = self.config.getint('connection_settings', 'update_interval')
        self.job_status_parser = JobStatusParser(self.base_uri)
        self.indicator = Indicator(name="Jenkins", icon=self.icon_success, description='Jenkins')
        self.update_status()
        gobject.timeout_add(self.update_interval, self.timer_callback)

    def item_callback(self, url):
        def cb():
            print url
            open_browser_command = ['/usr/bin/google-chrome', url]
            subprocess.call(open_browser_command)
        return cb

    def update_status(self):
        logging.debug("updating status")
        json_jobs = self.job_status_parser.parse()

        self.indicator.clear()
        tick = u'\u2713'
        cross = u'\u2718'
        def successful(job):
            return job['color'].startswith('blue')

        for json_job in json_jobs:
            color = json_job['color']
            name = json_job['name']
            success = successful(json_job)
            if(success):
                desc = "%s %s" % (tick, name)
            else:
                desc = "%s %s (%s)" % (cross, name, color)
            self.indicator.add_action(desc, self.item_callback(json_job['url']))
        any_failed = any([not successful(job) for job in json_jobs])
        icon = self.icon_error if any_failed else self.icon_success
        logging.debug("icon = %s" % (icon,))
        self.indicator.set_icon(icon)
          
        self.indicator.show()

    def quit(self):
        gtk.main_quit()

    def save_config(self, text):
        self.config.set("connection_settings", "base_uri", text)
        #self.config.write("app.properties")

    def timer_callback(self):
        if self.timeout_count % (self.timeout / 1000) == 0:
            self.timeout_count = 0
            self.update_status()
        self.timeout_count += 1
        return True

if __name__ == '__main__':
    JenkinsApplet()
    gtk.main()
