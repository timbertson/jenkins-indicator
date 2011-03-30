
import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk

class JenkinsStatus(object):
    def __init__(self, applet):
#        self.applet = applet
        self.create_button(applet)
        self.create_drawing_area(applet)
        
    def create_button(self, applet):
        self.button = gtk.Button()
	self.button.set_relief(gtk.RELIEF_NONE)
	self.button.set_label("status button")
	self.button.connect("button-press-event", self.show_menu, applet)

    def create_drawing_area(self, applet):
        self.area = gtk.DrawingArea()
        self.area.set_size_request(100,30)
        #        pixmap = gtk.gdk.Pixmap(self.area.window, 100, 30, depth=16)
        #        pixmap.draw_rectangle(applet.get_style().white_gc, True, 0, 0, 100, 30)
        self.area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.area.connect("button-press-event", self.area_clicked)

    def configure_event(widget, event):
        println("configure event")
        global pixmap

        x, y, width, height = widget.get_allocation()
        pixmap = gtk.gdk.Pixmap(widget.window, width, height)
        pixmap.draw_rectangle(widget.get_style().white_gc,
                              True, 0, 0, width, height)
        return True

    def expose_event(widget, event):
        println("expose event")
        x , y, width, height = event.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                    pixmap, x, y, x, y, width, height)
        return False

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
