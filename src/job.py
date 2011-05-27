#!/usr/bin/env python

import pygtk

pygtk.require('2.0')
import gtk
import logging
import subprocess
from job_images import JobImages

class Job(gtk.Button):
    LEFT_MOUSE_BUTTON = 1
    CENTRE_MOUSE_BUTTON = 2
    RIGHT_MOUSE_BUTTON = 3

    def __init__(self, name, color, url, config, max_image_size):
        gtk.Button.__init__(self)
        self.job_images = JobImages(config, max_image_size)
        self.max_image_size = max_image_size
        self.config = config
        self.job_name = name.strip()
        self.color = color.strip()
        self.url = url.strip()
        #self.menu = menu
        #self.set_relief(gtk.RELIEF_NONE)
        self.set_tooltip_text(self.job_name + ":" + self.color)
        self.connect("clicked", self.button_clicked, "some data")
        self.connect("button_press_event", self.button_pressed, "some data")
        self.setup(self.job_name, self.color, self.url, True)

    def setup(self, name, color, url, reload=False):
        logging.debug("self.color: " + self.color)
        if (reload or self.color != color):
            logging.debug("self.color has changed")
            for child in self.get_children():
                self.remove(child)
                #child.unparent()
            self.add(self.job_images.get(color))
        else:
            logging.debug("self.color hasn't changed")

    def button_clicked(self, button, data=None):
        logging.debug("button pressed in job " + self.job_name)
        open_browser_command = '/usr/bin/google-chrome' + self.url
        #os.system(open_browser_command)
        subprocess.call(open_browser_command, shell=False)

    def button_pressed(self, widget, event, parameters=None):
        logging.debug('button press')
        if event.button == self.LEFT_MOUSE_BUTTON:
            logging.debug('left button')
        elif event.button == self.CENTRE_MOUSE_BUTTON:
            logging.debug('centre button')
        elif event.button == self.RIGHT_MOUSE_BUTTON:
            logging.debug('right button')
            self.menu.show(widget, event)

if __name__ == '__main__':
    parser = JobStatusParser()
    jobs = parser.build()
    for job in jobs:
        logging.debug("name: " + job.job_name + ", " + job.color)

