import pygtk
pygtk.require('2.0')
import gtk
import gobject
import gnome
import gnomeapplet
import sys
import gc
import logging
from job_status import JobStatus

class JenkinsApplet(gnomeapplet.Applet):
    LEFT_MOUSE_BUTTON=1
    RIGHT_MOUSE_BUTTON=2

    def __init__(self, applet, iid):
        self.applet = applet
        self.job_status = JobStatus()

        self.check_job_status()
	self.timeout = 5000
        self.timeout_count = 1

        self.box = self.create_applet()
    
        self.update_buttons()
			
        self.timeout_source = gobject.timeout_add (6000, self.update_main)
        self.update_main

 	self.applet.connect("button-press-event", self.show_menu, self.applet)

        #self.applet.connect('button-press-event', self.button_press)
        #self.applet.connect("change_background", self.change_background)
        #self.applet.connect("change-orient", self.change_orientation)

    def check_job_status(self):
        self.jobs = self.job_status.build()

    def create_applet(self):
        app_window = self.applet
        
        event_box = gtk.EventBox()
        event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK | 
                             gtk.gdk.POINTER_MOTION_MASK | 
                             gtk.gdk.POINTER_MOTION_HINT_MASK |
                             gtk.gdk.CONFIGURE )

        self.buttons = []
        for job in self.jobs:
            button = gtk.Button(job.name)
            self.buttons.append(button)
        self.update_buttons()

        self.text = gtk.Label()
        self.text.show()
        self.text.set_text("Stat")
		
        self.inside_applet = gtk.HBox()
        self.inside_applet.pack_start(self.text)
        for button in self.buttons:
            self.inside_applet.pack_start(button)
            
        event_box.add(self.inside_applet)
        app_window.add(event_box)
        app_window.show_all()
        return event_box

    def update_buttons(self):
        for i in range(0, len(self.buttons)):
            self.update_button(self.buttons[i], self.jobs[i])

    def update_button(self, button, job):
        self.set_color(button, job.color)
        button.show()
        button.set_label(job.name)

    def set_color(self, button, color):
        map = button.get_colormap() 
        color = map.alloc_color(color)
        style = button.get_style().copy()
        style.bg[gtk.STATE_NORMAL] = color
        button.set_style(style)

    def update_main(self):
        if self.timeout_count % (self.timeout / 1000) == 0:
            self.timeout_count = 0
            self.update_status()
        self.timeout_count += 1
        return True

    def update_status(self):
        print("updating status")
        self.check_job_status()
        self.update_buttons()

    def button_press(self, button, event):
        if event.button == self.LEFT_MOUSE_BUTTON:
            logging.debug('left button')
        elif event.button == self.RIGHT_MOUSE_BUTTON:
            logging.debug('right button')
            self.show_menu(button, event, self.applet)

    def show_menu(self, widget, event, applet):
        print("show menu")
	if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            print "Button3"
            widget.emit_stop_by_name("button_press_event")
            self.create_menu(applet)

    def create_menu(self, applet):
	propxml="""<popup name="button3">
		       <menuitem name="Item 3" verb="About" label="_About" 
                             pixtype="stock" pixname="gtk-about"/>
		   </popup>"""
	verbs = [("About", self.show_about_dialog)]
	applet.setup_menu(propxml, verbs, None)  

    def show_about_dialog(self, *arguments, **keywords):
	print "Showing about dialog"
	pass

def jenkins_applet_factory(applet, iid):
	JenkinsApplet(applet, iid)
	return True

if len(sys.argv) == 2:
	if sys.argv[1] == "window":
            print("Running in a window")
            mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
            mainWindow.set_title("Debug Window of JenkinsApplet")
            mainWindow.connect("destroy", gtk.main_quit)
            applet = gnomeapplet.Applet()
            jenkins_applet_factory(applet, None)
            applet.reparent(mainWindow)
            mainWindow.show_all()
            gtk.main()
            sys.exit()

if __name__ == '__main__':
	print "Starting factory"
	gnomeapplet.bonobo_factory("OAFIID:Jenkins_Applet_Factory", 
                                   JenkinsApplet.__gtype__, 
                                   "JenkinsApplet", 
                                   "1.0", 
                                   jenkins_applet_factory)
