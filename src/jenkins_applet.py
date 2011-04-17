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
from images import Images

class JenkinsApplet(gnomeapplet.Applet):
    LEFT_MOUSE_BUTTON=1
    CENTRE_MOUSE_BUTTON=2
    RIGHT_MOUSE_BUTTON=3
    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, applet, iid):
        self.config = ConfigParser.ConfigParser()  
        self.applet = applet
        self.jobs = []
        self.max_image_size = self.applet.get_size() - 2

        self.reload_config()

	self.timeout = 5000
        self.timeout_count = 1
			
        gobject.timeout_add(self.update_interval, self.timer_callback)
        self.timer_callback

    def reload_config(self):
        self.config.read("app.properties")  

        self.images = Images(self.config)
        self.base_uri = self.config.get('connection_settings','base_uri')
        self.job_status_parser = JobStatusParser(self.base_uri, self.images, self.max_image_size)
        self.update_interval = self.config.getint('connection_settings', 'update_interval')
        self.update_status()
        self.box = self.create_applet()

    def update_status(self):
        logging.debug("updating status")
        self.jobs = self.job_status_parser.build(self.config)

    def save_config(self, text):
        self.config.set("connection_settings", "base_uri", text)
        #self.config.write("app.properties")

    def create_applet(self):
        event_box = gtk.EventBox()
        event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK | 
                             gtk.gdk.POINTER_MOTION_MASK | 
                             gtk.gdk.POINTER_MOTION_HINT_MASK |
                             gtk.gdk.CONFIGURE )

        inside_applet = gtk.HBox()
        for job in self.jobs:
            inside_applet.pack_start(job.icon)
            
        event_box.add(inside_applet)
        event_box.connect('button-press-event', self.button_press)
        self.applet.add(event_box)
        self.applet.show_all()
        return event_box

    def timer_callback(self):
        if self.timeout_count % (self.timeout / 1000) == 0:
            self.timeout_count = 0
            self.update_status()
        self.timeout_count += 1
        return True

    def button_press(self, widget, event):
        if event.button == self.LEFT_MOUSE_BUTTON:
            logging.debug('left button')
        elif event.button == self.CENTRE_MOUSE_BUTTON:
            logging.debug('centre button')
        elif event.button == self.RIGHT_MOUSE_BUTTON:
            logging.debug('right button')
            self.show_menu(widget, event, self.applet)

    def show_menu(self, widget, event, applet):
        logging.debug("show menu")
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == self.RIGHT_MOUSE_BUTTON:
            logging.debug("right menu button")
            widget.emit_stop_by_name("button_press_event")
            self.create_menu(applet)

    def create_menu(self, applet):
        propxml=        """<popup name="button3">
        <menuitem name="Item 3" verb="Config" label="_Config" 
        pixtype="stock" pixname="gtk-about"/>
        </popup>"""
        verbs = [("Config", self.show_config_dialog)]
        applet.setup_menu(propxml, verbs, None)  

    def show_config_dialog(self, *arguments, **keywords):
        builder = ConfigDialogBuilder(self, self.base_uri)
        dialog = builder.build()
        dialog.show()

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
