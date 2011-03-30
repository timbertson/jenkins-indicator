#!/usr/bin/env python

import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk
from jenkins_status import JenkinsStatus

def factory(applet, something):
    status = JenkinsStatus(applet)

    hbox = gtk.HBox()
    hbox.add(status.button)
    hbox.add(status.area)
    applet.add(hbox)

    applet.show_all()
    return True

if len(sys.argv) == 2:
	if sys.argv[1] == "run-in-window":
		mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		mainWindow.set_title("Ubuntu System Panel")
		mainWindow.connect("destroy", gtk.main_quit)
		applet = gnomeapplet.Applet()
		factory(applet, None)
		applet.reparent(mainWindow)
		mainWindow.show_all()
		gtk.main()
		sys.exit()

if __name__ == '__main__':
	print "Starting factory"
	gnomeapplet.bonobo_factory("OAFIID:My_Factory", gnomeapplet.Applet.__gtype__, "My_New_Applet", "1.0", factory)
