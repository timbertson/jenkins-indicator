import pygtk
pygtk.require('2.0')
import gtk
import gobject
import gnome
import gnomeapplet
import sys
import gc
import logging

class MyApplet(gnomeapplet.Applet):
    LEFT_MOUSE_BUTTON=1
    RIGHT_MOUSE_BUTTON=2

    def __init__(self,applet,iid):
        self.build_passed = False
        print("init")
        self.applet = applet

	self.timeout = 5000
        self.timeout_count = 1

        # Lets create the gui
        self.box = self.create_applet()
        
        # Show icon
        self.update_icon()
			
        # Callbacks for timeout and change_background and orientation
        self.timeout_source = gobject.timeout_add (1000, self.update_main)
        #self.applet.connect("change_background", self.change_background)
        #self.applet.connect("change-orient", self.change_orientation)
        self.applet.connect('button-press-event', self.button_press)

    def toggle_build_passed(self):
        self.build_passed = not self.build_passed

    # Draws applet
    def create_applet(self):
        app_window = self.applet
        
        event_box = gtk.EventBox()
        event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK | 
                             gtk.gdk.POINTER_MOTION_MASK | 
                             gtk.gdk.POINTER_MOTION_HINT_MASK |
                             gtk.gdk.CONFIGURE )
		
        # Creates icon for applet
        self.icon = gtk.Image()
        self.update_icon()
		
        # Create label for temp
        self.temp = gtk.Label()
        self.update_text()
		
        # Creates hbox with icon and temp
        self.inside_applet = gtk.HBox()
        self.inside_applet.pack_start(self.icon)
        self.inside_applet.pack_start(self.temp)
            
        # Creates tooltip
        self.tooltip = gtk.Tooltip()
        self.update_tooltip()
		
        # Adds hbox to eventbox
        event_box.add(self.inside_applet)
        app_window.add(event_box)
        app_window.show_all()
        return event_box

    # Update applet icon depending on temperature
    def update_icon(self):
        self.icon.show()

        if self.build_passed:
            self.icon_path = "/usr/share/pixmaps/monitor.png"
            self.set_icon(self.icon_path)
        else:
            self.icon_path = "/usr/share/pixmaps/nobody.png"
            self.set_icon(self.icon_path)

    def set_icon(self, path):
        self.icon.clear()
        gc.collect()
        self.icon.set_from_file(self.icon_path)

    def update_text(self):
        self.temp.show()
        self.temp.set_text("some text")

    def update_tooltip(self):
        self.tooltip.set_text("tooltip text")

    def update_main(self):
        if self.timeout_count % (self.timeout / 1000) == 0:
            self.timeout_count = 0
            self.update_status()
        self.timeout_count += 1
            
        return True

    # Update data displayed on icon
    def update_status(self):
        print("updating temp")
        self.update_icon()
        self.update_text()
        self.update_tooltip()

    def button_press(self, button, event):
        if event.button == self.LEFT_MOUSE_BUTTON:
            print("left")
            self.toggle_build_passed()
        elif event.button == self.RIGHT_MOUSE_BUTTON:
            print("right")
            
def myapplet_factory(applet, iid):
	MyApplet(applet, iid)
	return True

if len(sys.argv) == 2:
	if sys.argv[1] == "window":
            print("Running in a window")
            mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
            mainWindow.set_title("Debug Window of MyApplet")
            mainWindow.connect("destroy", gtk.main_quit)
            applet = gnomeapplet.Applet()
            myapplet_factory(applet, None)
            applet.reparent(mainWindow)
            mainWindow.show_all()
            gtk.main()
            sys.exit()

if __name__ == '__main__':
	print "Starting factory"
	gnomeapplet.bonobo_factory("OAFIID:My_Factory", 
                                   MyApplet.__gtype__, 
                                   "MyApplet", 
                                   "1.0", 
                                   myapplet_factory)
