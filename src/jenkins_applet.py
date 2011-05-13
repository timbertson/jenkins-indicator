#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import gnome
import gnomeapplet
import sys
import gc
import logging
import os
import ConfigParser  
from config_dialog_builder import ConfigDialogBuilder
from job_status_parser import JobStatusParser
from setup_menu import SetupMenu
from icon_types import IconTypes

class JenkinsApplet(gnomeapplet.Applet):
    LEFT_MOUSE_BUTTON=1
    CENTRE_MOUSE_BUTTON=2
    RIGHT_MOUSE_BUTTON=3
    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, applet, iid):
        #settings = gtk.settings_get_default()
        #settings.set_string_property("gtk-button-images", "True", "blah")
        self.config = ConfigParser.ConfigParser()  
        self.applet = applet
        self.jobs = []
        self.max_image_size = self.applet.get_size() - 2
        self.menu = SetupMenu(self)
	self.timeout = 5000
        self.timeout_count = 1
        self.images = JobImages()
        self.load_config()
        self.timer_callback
        gobject.timeout_add(self.update_interval, self.timer_callback)

    def load_config(self):
        self.config.read("app.properties")  
        self.base_uri = self.config.get('connection_settings','base_uri')
        self.job_status_parser = JobStatusParser(self.base_uri, self.job_images, self.max_image_size, self.menu)
        self.update_interval = self.config.getint('connection_settings', 'update_interval')
        self.update_status()
        self.box = self.create_applet()

    def reload_config(self):
        self.update_status()
        #self.box = self.create_applet()

    def update_status(self):
        logging.debug("updating status")
        json = self.job_status_parser.build(self.config)

        create_new_jobs = false
        if(len(self.jobs) != len(json_jobs)):
            print("Number of jobs has changed")
            self.jobs = []
            for i in range(len(json_jobs)):
                json = json_jobs[i]
                job = Job(json_job.get("name")[0:20], json_job.get("color"), json_job.get("url"), 
                          config, self.images, self.max_image_size, self.menu)
                self.jobs.append(job)
        else:
            print("Number of jobs is the same")
            for i in range(len(json_jobs)):
                job = self.jobs[i]
                json = json_jobs[i]
                
                color = json_job.get("color")
                job.setup(json_job.get("name")[0:20], color, json_job.get("url"), self.job_images(color))

        print("jobs: "+str(self.jobs))

    def save_config(self, text):
        self.config.set("connection_settings", "base_uri", text)
        #self.config.write("app.properties")

    def create_applet(self):
        inside_applet = gtk.HBox()
        #setup_label = SetupLabel()
        #setup_label.setup()
        #inside_applet.pack_start(setup_label)
        for job in self.jobs:
            inside_applet.pack_start(job)
        self.applet.add(inside_applet)
        self.applet.show_all()
        #setup_label.connect('button-press-event', self.button_press, "parameters")
        return inside_applet

    def timer_callback(self):
        if self.timeout_count % (self.timeout / 1000) == 0:
            self.timeout_count = 0
            self.update_status()
        self.timeout_count += 1
        return True

    def button_press(self, widget, event, parameters = None):
        logging.debug('button press')
        if event.button == self.LEFT_MOUSE_BUTTON:
            logging.debug('left button')
        elif event.button == self.CENTRE_MOUSE_BUTTON:
            logging.debug('centre button')
        elif event.button == self.RIGHT_MOUSE_BUTTON:
            logging.debug('right button')
            self.show_menu(widget, event, self.applet)

def jenkins_applet_factory(applet, iid):
    JenkinsApplet(applet, iid)
    return True

if len(sys.argv) == 2:
    if sys.argv[1] == "window":
        logging.debug("Running in a window")

        mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mainWindow.set_title("Debug Window of JenkinsApplet")
        mainWindow.connect("destroy", gtk.main_quit)
        applet = gnomeapplet.Applet()
        jenkins_applet_factory(applet, None)
        applet.reparent(mainWindow)
        mainWindow.show_all()
        gtk.main()
        sys.exit()

if __name__ == '__main__':
    logging.debug("Starting factory")
    gnomeapplet.bonobo_factory("OAFIID:Jenkins_Applet_Factory", 
                               JenkinsApplet.__gtype__, 
                               "JenkinsApplet", 
                               "1.0", 
                               jenkins_applet_factory)
