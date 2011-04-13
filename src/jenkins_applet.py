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
from job_status import JobStatus

class JenkinsApplet(gnomeapplet.Applet):
    LEFT_MOUSE_BUTTON=1
    RIGHT_MOUSE_BUTTON=2
    
    blue_image = '/usr/share/icons/gnome/24x24/apps/gnome-window-manager.png'
    red_anime_image = '/usr/share/icons/gnome/24x24/apps/volume-knob.png'
    red_image = '/usr/share/icons/gnome/24x24/apps/terminal.png'
    unknown_image = '/usr/share/icons/gnome/24x24/apps/susehelpcenter.png'

    def __init__(self, applet, iid):
        self.applet = applet
        self.size = self.applet.get_size() - 2
        self.job_status = JobStatus()

        self.check_job_status()
	self.timeout = 5000
        self.timeout_count = 1

        self.box = self.create_applet()
        self.update_status()
        self.update_icons()
			
        self.timeout_source = gobject.timeout_add (6000, self.update_main)
        self.update_main

 	#self.applet.connect("button-press-event", self.show_menu, self.applet)
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

        self.icons = []
        for job in self.jobs:
            icon = gtk.Image() 
            self.update_icon(icon, job)
            icon.connect('button-press-event', self.icon_press)
            icon.set_tooltip_text(job.name)
            self.icons.append(icon)
        self.update_icons()

        self.inside_applet = gtk.HBox()
        for icon in self.icons:
            self.inside_applet.pack_start(icon)
            
        event_box.add(self.inside_applet)
        app_window.add(event_box)
        app_window.show_all()
        return event_box
    
    def update_image(self, icon, image_file):
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(image_file, self.size, self.size)
        icon.set_from_pixbuf(pixbuf)

    def update_icons(self):
        for icon, job in zip(self.icons, self.jobs):
            self.update_icon(icon, job)

    def update_icon(self, icon, job):
        self.set_color(icon, job.color)
        icon.show()
        icon.set_tooltip_text(job.name + " (" +job.color+")")

    def set_color(self, icon, job_color):
        if job_color == "blue":
            self.update_image(icon, self.blue_image)
        if "red_anime" == job_color:
            self.update_image(icon, self.red_anime_image)
        elif "red" in job_color:
            self.update_image(icon, self.red_image)
        else:
            self.update_image(icon, self.unknown_image)

    def update_main(self):
        if self.timeout_count % (self.timeout / 1000) == 0:
            self.timeout_count = 0
            self.update_status()
        self.timeout_count += 1
        return True

    def update_status(self):
        logging.debug("updating status")
        self.check_job_status()
        self.update_icons()
        #self.update_buttons()

    def icon_press(self, button, event):
        logging.debug("button press "+button.get_label())
        if event.button == self.LEFT_MOUSE_BUTTON:
            logging.debug('left button')
            os.system('xdg-open http://localhost:18080')
        elif event.button == self.RIGHT_MOUSE_BUTTON:
            logging.debug('right button')
            #self.show_menu(button, event, self.applet)

    #def show_menu(self, widget, event, applet):
    #    if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
    #        logging.debug("Button3")
    #        widget.emit_stop_by_name("button_press_event")
    #        self.create_menu(applet)

    #def create_menu(self, applet):
    #    propxml="""<popup name="button3">
    #    <menuitem name="Item 3" verb="About" label="_About" 
    #                         pixtype="stock" pixname="gtk-about"/>
    #</popup>"""
    #verbs = [("About", self.show_about_dialog)]
    #applet.setup_menu(propxml, verbs, None)  

    def show_about_dialog(self, *arguments, **keywords):
	logging.debug("Showing about dialog")
	pass

def jenkins_applet_factory(applet, iid):
    JenkinsApplet(applet, iid)
    return True

if len(sys.argv) == 2:
    if sys.argv[1] == "window":
        logging.debug("Running in a window")
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
    logging.debug("Starting factory")
    gnomeapplet.bonobo_factory("OAFIID:Jenkins_Applet_Factory", 
                               JenkinsApplet.__gtype__, 
                               "JenkinsApplet", 
                               "1.0", 
                               jenkins_applet_factory)
