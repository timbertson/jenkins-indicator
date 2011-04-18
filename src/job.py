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
import subprocess
from images import Images

class Job(gtk.Button):
    LEFT_MOUSE_BUTTON=1
    CENTRE_MOUSE_BUTTON=2
    RIGHT_MOUSE_BUTTON=3

    def __init__(self, name, color, url, config, images, max_image_size, menu):
        gtk.Button.__init__(self)
        self.max_image_size = max_image_size
        self.config = config
        self.job_name = name.strip()
        self.color = color.strip()
        self.url = url.strip()
        self.images = images
        self.menu = menu
	#self.set_relief(gtk.RELIEF_NONE)
        self.set_tooltip_text(self.job_name)
        self.__setup_image(gtk.Image())
        self.connect("clicked", self.button_clicked, "some data")
        self.connect("button_press_event", self.button_pressed, "some data")
        
    def button_clicked(self, button, data=None):
        logging.debug("button pressed in job "+self.job_name)
        open_browser_command  = '/usr/bin/google-chrome'+self.url
        #os.system(open_browser_command)
        subprocess.call(open_browser_command, shell=False)

    def button_pressed(self, widget, event, parameters = None):
        logging.debug('button press')
        if event.button == self.LEFT_MOUSE_BUTTON:
            logging.debug('left button')
        elif event.button == self.CENTRE_MOUSE_BUTTON:
            logging.debug('centre button')
        elif event.button == self.RIGHT_MOUSE_BUTTON:
            logging.debug('right button')
            self.menu.show(widget, event)

    def __setup_image(self, image):
        color_file = self.__choose_color_file()
        data = self.__load_image_data(color_file)
        image.set_from_pixbuf(data)
        # is this required?
        self.add(image)

    def __choose_color_file(self):
        if "blue" == self.color:
            return self.images.blue_image
        elif "blue_anime" == self.color:
            return self.images.blue_anime_image
        elif "red_anime" == self.color:
            return self.images.red_anime_image
        elif "red" == self.color:
            return self.images.red_image
        elif "disabled" == self.color:
            return self.images.disabled_image
        else:
            logging.debug("unknown color: \""+self.color+"\"")
            return self.unknown_image

    def __load_image_data(self, image_file):
        return gtk.gdk.pixbuf_new_from_file_at_size(image_file, self.max_image_size, self.max_image_size)

if __name__ == '__main__':
    parser = JobStatusParser()
    jobs = parser.build()
    for job in jobs:
        logging.debug("name: "+job.job_name+", "+job.color)

