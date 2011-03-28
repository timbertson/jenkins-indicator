import pygtk
import sys
pygtk.require('2.0')
import gtk

import gnomeapplet
import gtk

class Status:
    def __init__(self):
	button = gtk.Button()
	button.set_relief(gtk.RELIEF_NONE)
	button.set_label("ExampleButton")
	button.connect("button-press-event", show_menu, applet)

    def create_menu(applet):
	print "Creating menu"
	propxml="""
			<popup name="button3">
			<menuitem name="Item 3" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
			</popup>"""
	verbs = [("About", show_about_dialog)]
	applet.setup_menu(propxml, verbs, None)

    def show_menu(widget, event, applet):
	print "Showing menu"
	if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
		print "Button3"
		widget.emit_stop_by_name("button_press_event")
		create_menu(applet)

    def show_about_dialog(*arguments, **keywords):
	print "Showing about dialog"
	pass
