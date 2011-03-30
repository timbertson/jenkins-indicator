
import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk

class JenkinsStatus(object):
    def __init__(self, applet, iid):
        self.applet = applet
        self.setup()

    def setup(self): 
        self.create_button()
        self.create_drawing_area()
        
    def create_button(self):
        self.button = gtk.Button()
	self.button.set_relief(gtk.RELIEF_NONE)
	self.button.set_label("status button")
	self.button.connect("button-press-event", self.show_menu, self.applet)

    def create_drawing_area(self):
        self.area = gtk.DrawingArea()
        self.area.set_size_request(100,30)
        self.draw_pixmap()
        self.area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.area.connect("button-press-event", self.area_clicked)

    def draw_pixmap(self):
        pixmap = gtk.gdk.Pixmap(self.area.window, 100, 30, depth=16)
        self.gc = self.create_gc()
        pixmap.draw_rectangle(self.gc, True, 0, 0, 100, 30)

    def create_gc(self):
        red = gtk.gdk.Color(red=255, green=0, blue=0, pixel=0)
        gc = self.area.window.new_gc(foreground=red)
        
    def configure_event(self, event):
        println("configure event")
    #     global pixmap

    #     x, y, width, height = self.get_allocation()
    #     pixmap = gtk.gdk.Pixmap(self.window, width, height)
    #     pixmap.draw_rectangle(self.get_style().white_gc,
    #                           True, 0, 0, width, height)
    #     return True

    def expose_event(self, event):
        println("expose event")
    #     x , y, width, height = event.area
    #     widget.window.draw_drawable(self.get_style().fg_gc[gtk.STATE_NORMAL],
    #                                 pixmap, x, y, x, y, width, height)
    #     return False

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
