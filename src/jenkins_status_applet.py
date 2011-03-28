#!/usr/bin/env python

import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk

class JenkinsStatus(object):
    def __init__(self, applet):
        self.create_button()
        self.create_drawing_area(applet)
        self.create_color_button()

    def create_color_button(self):
        self.color_button = gtk.Button()
        self.color_button.set_label("colour")
        
    def create_button(self):
        self.button = gtk.Button()
	self.button.set_relief(gtk.RELIEF_NONE)
	self.button.set_label("status button")
	self.button.connect("button-press-event", self.show_menu, applet)

    def create_drawing_area(self, applet):
        self.area = gtk.DrawingArea()
        self.area.set_size_request(100,30)
        #        pixmap = gtk.gdk.Pixmap(applet.window, 100, 30, depth=-1)
        #        pixmap.draw_rectangle(applet.get_style().white_gc, True, 0, 0, width, height)
        self.area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.area.connect("button-press-event", self.area_clicked)

    def area_clicked(self, widget, event):
        print "area clicked"

    def create_menu(self, applet):
	print "Creating menu"
	propxml="""
			<popup name="button3">
			<menuitem name="Item 3" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
			</popup>"""
	verbs = [("About", self.show_about_dialog)]
	applet.setup_menu(propxml, verbs, None)

    def show_menu(self, widget, event, applet):
	print "Showing menu"
	if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
		print "Button3"
		widget.emit_stop_by_name("button_press_event")
		self.create_menu(applet)

    def show_about_dialog(self, *arguments, **keywords):
	print "Showing about dialog"
	pass

def factory(applet, iid):
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
