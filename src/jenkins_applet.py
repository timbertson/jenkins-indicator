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

    #PASSED_IMAGE = "/home/james/projects/Jenkins-Gnome-Applet/images/camellia_passed.png"
    #FAILED_IMAGE = "/home/james/projects/Jenkins-Gnome-Applet/images/camellia_failed.png"

    def __init__(self, applet, iid):
        self.applet = applet
        #self.build_passed = False
        self.job_status = JobStatus()

        self.check_job_status()

        #self.passed_image = gtk.Image()
        #self.passed_image.set_from_file(self.PASSED_IMAGE)
        #self.failed_image = gtk.Image()
        #self.failed_image.set_from_file(self.FAILED_IMAGE)

	self.timeout = 5000
        self.timeout_count = 1

        self.box = self.create_applet()
    
        #self.update_icons()
        self.update_buttons()
			
        #self.applet.connect('button-press-event', self.button_press)
        self.timeout_source = gobject.timeout_add (6000, self.update_main)
        self.update_main
        #self.applet.connect("change_background", self.change_background)
        #self.applet.connect("change-orient", self.change_orientation)

        #self.update_button_color(self.buttons[0])
        #self.update_button_color(self.buttons[1])

    def check_job_status(self):
        self.jobs = self.job_status.build()

    # Draws applet
    def create_applet(self):
        app_window = self.applet
        
        event_box = gtk.EventBox()
        event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK | 
                             gtk.gdk.POINTER_MOTION_MASK | 
                             gtk.gdk.POINTER_MOTION_HINT_MASK |
                             gtk.gdk.CONFIGURE )
		
        # Creates icon for applet
        #self.icons = [gtk.Image(), gtk.Image()]
        #self.update_icons()

        self.buttons = []
        for job in self.jobs:
            button = gtk.Button(job.name)
            button.set_size_request(150,50)
            self.buttons.append(button)
        self.update_buttons()

        # Create label for temp
        self.text = gtk.Label()
        self.text.show()
        self.text.set_text("Status")
        #self.update_text()
		
        # Creates hbox with icon and temp
        self.inside_applet = gtk.HBox()
        #self.inside_applet.pack_start(self.icons[0])
        #self.inside_applet.pack_start(self.icons[1])
        self.inside_applet.pack_start(self.buttons[0])
        self.inside_applet.pack_start(self.buttons[1])
        self.inside_applet.pack_start(self.text)
            
        # Creates tooltip
        #self.tooltip = gtk.Tooltip()
        #self.update_tooltip()

        # Adds hbox to eventbox
        event_box.add(self.inside_applet)
        app_window.add(event_box)
        app_window.show_all()
        return event_box

    def update_buttons(self):
        for i in range(0, len(self.buttons)):
            self.update_button(self.buttons[i], self.jobs[i])

    def update_button(self, button, job):
        #set the button's style to the one you created
        #self.update_button_color(button)
        button.show()
        button.set_label(job.name+": "+job.color)

    def update_main(self):
        if self.timeout_count % (self.timeout / 1000) == 0:
            self.timeout_count = 0
            self.update_status()
        self.timeout_count += 1
        return True

    # Update data displayed on icon
    def update_status(self):
        print("updating status")
        self.check_job_status()
        self.update_buttons()
        #self.update_icons()
        #self.update_text()
        #self.update_tooltip()

    #def update_button_color(self, button): 
    #    color_map = button.get_colormap() 
    #    color = color_map.alloc_color(self.get_build_color())
    #    style = button.get_style().copy()
    #    style.bg[gtk.STATE_NORMAL] = color

    #def get_build_color(self):
    #    if self.build_passed: 
    #        return "green" 
    #    else: 
    #        return "red"

    #def set_build_passed(self, new_status):
    #    print("setting build_passed: "+str(new_status))
    #    self.build_passed = new_status

    # Update applet icon depending on temperature
    #def update_icons(self):
    #    for icon in self.icons:
    #        self.update_icon(icon)

    #def update_icon(self, icon):
    #    icon.show()
    #    if self.build_passed:
    #        self.set_icon(icon, self.PASSED_IMAGE)
    #    else:
    #        self.set_icon(icon, self.FAILED_IMAGE)
    
    #def set_icon(self, icon, path):
    #    icon.clear()
    #    gc.collect()
    #    icon.set_from_file(path)

    #def update_text(self):
    #    self.temp.show()
    #    self.temp.set_text("some text")

    #def update_tooltip(self):
    #    self.tooltip.set_text("tooltip text")

    #def check_status(self):
    #    self.set_build_passed(self.status_parser.get_build_colour() == "blue")

    #def button_press(self, button, event):
    #    if event.button == self.LEFT_MOUSE_BUTTON:
    #        print("left")
    #        self.set_build_passed(True)
    #    else:
    #        print("right")
    #        self.set_build_passed(False)
            
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
