
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

class SetupMenu:
    LEFT_MOUSE_BUTTON=1
    CENTRE_MOUSE_BUTTON=2
    RIGHT_MOUSE_BUTTON=3

    def __init__(self, applet):
        self.applet = applet

    def show(self, widget, event):
        logging.debug("show menu")
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == self.RIGHT_MOUSE_BUTTON:
            logging.debug("right menu button")
            widget.emit_stop_by_name("button_press_event")
            self.__create_menu()

    def __create_menu(self):
        propxml=        """<popup name="button3">
        <menuitem name="Item 3" verb="Config" label="_Config" 
        pixtype="stock" pixname="gtk-about"/>
        </popup>"""
        verbs = [("Config", self.__show_config_dialog)]
        #self.applet.setup_menu(propxml, verbs, None)  

    def __show_config_dialog(self, *arguments, **keywords):
        builder = ConfigDialogBuilder(self, self.base_uri)
        dialog = builder.build()
        dialog.show()
