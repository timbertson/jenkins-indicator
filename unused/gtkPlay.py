#!/usr/bin/env python

import pygtk
import sys
pygtk.require('2.0')
import gtk

class GtkPlay:
	def __init__(self):
		print "init"

	def showDrawingArea(self):
		print "show drawing area"
		area = gtk.DrawingArea()
		area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		area.connect("button-press-event", self.on_clicked)

	def on_clicked(self):
		print "clicked"

	def showButton(self):
		print "showButton"
		button = gtk.Button()
		button.set_relief(gtk.RELIEF_NONE)
		button.set_label("ExampleButton")
		#button.connect("button_press_event", showMenu, applet)
		
	def setupWindow(self):
		print "setupWindow"
		mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		mainWindow.set_title("GTK Play")
		mainWindow.connect("destroy", gtk.main_quit)
		mainWindow.show_all()
		gtk.main()
		sys.exit()

if __name__ == '__main__':
	print "main"
	Play = GtkPlay()
	Play.showDrawingArea()
	Play.setupWindow()

