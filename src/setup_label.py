
import pygtk
pygtk.require('2.0')
import gtk
import logging

class SetupLabel(gtk.EventBox):
    def setup(self):
        self.set_events(gtk.gdk.BUTTON_PRESS_MASK | 
                        gtk.gdk.POINTER_MOTION_MASK | 
                        gtk.gdk.POINTER_MOTION_HINT_MASK |
                        gtk.gdk.CONFIGURE)
        self.add(gtk.Label("Setup"))
        self.show_all()
