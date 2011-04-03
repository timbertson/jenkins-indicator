
import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk
import logging

class JenkinsStatus(object):
    title = "Jenkins Status"
    image_file = '/usr/share/icons/gnome/24x24/apps/gnome-window-manager.png'
    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, applet, iid):
        self.applet = applet
        print("Applet size is: ")
        print(applet.get_size())
        self.setup()

    def setup(self): 
        self.create_icon()
        # self.create_button()
        # self.create_drawing_area()
        # self.setup_tooltips()

    # def setup_tooltips(self):
    #     tooltips = gtk.Tooltips()
    #     tooltips.set_tip(image, self.title)

    def create_icon(self):
        self.icon.show()

        #self.set_image()
        #self.applet.connect('button-press-event', self.button_press)
        #self.applet.connect('change-size', self.change_size, self.image)
        #self.applet.connect('change-background', self.change_background)
        #self.applet.show_all()

    def button_press(self, button, event):
        logging.debug('button_press')
        # left mouse button
        if event.button == 1:
            logging.debug('show guests')
            self.set_image()
        # right mouse button
        elif event.button == 2:
            logging.debug('show options')

    def set_image(self):
        size = self.applet.get_size() -2
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.image_file, size, size)
        self.image = gtk.Image()
        self.image.set_from_pixbuf(pixbuf)
        self.applet.add(self.image)

    # when the applet window changes size
    def change_size(self, applet, new_size, image):
        logging.debug('change_size')

        self.do_image(self.image_file, image)

    # when the theme background changes
    def change_background(self, applet, type, color, pixmap):
        logging.debug('change_background')

        applet.set_style(None)
        applet.modify_style(gtk.RcStyle())

        if type == gnomeapplet.COLOR_BACKGROUND:
            applet.modify_bg(gtk.STATE_NORMAL, color)
        elif type == gnomeapplet.PIXMAP_BACKGROUND:
            applet.get_style().bg_pixmap[gtk.STATE_NORMAL] = pixmap


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
