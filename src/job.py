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
from images import Images

class Job:
    def __init__(self, name, color, url, config, images, max_image_size):
        self.max_image_size = max_image_size
        self.config = config
        self.name = name.strip()
        self.color = color.strip()
        self.url = url.strip()
        self.images = images
        self.create_icon()

    def create_icon(self):
        self.icon = gtk.Image()
        self.icon.set_tooltip_text(self.name)
        self.__set_color()
        self.icon.show()
        self.icon.set_tooltip_text(self.name + " (" +self.color+")")
        
    def __set_color(self):
        logging.debug("job_color: "+self.color)
        if "blue" == self.color:
            self.__update_image(self.images.blue_image)
        elif "blue_anime" == self.color:
            self.__update_image(self.images.blue_anime_image)
        elif "red_anime" == self.color:
            self.__update_image(self.images.red_anime_image)
        elif "red" == self.color:
            self.__update_image(self.images.red_image)
        elif "disabled" == self.color:
            self.__update_image(self.images.disabled_image)
        else:
            logging.debug("unknown color: \""+self.color+"\"")
            self.update_image(self.icon, self.unknown_image)

    def __update_image(self, image_file):
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(image_file, self.max_image_size, self.max_image_size)
        self.icon.set_from_pixbuf(pixbuf)

if __name__ == '__main__':
    parser = JobStatusParser()
    jobs = parser.build()
    for job in jobs:
        logging.debug("name: "+job.name+", "+job.color)

