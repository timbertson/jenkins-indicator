import pygtk
pygtk.require('2.0')
import gtk
import gobject
import gnome
import gnomeapplet
import logging

class ConfigDialogBuilder:
    def __init__(self, applet, base_uri):
        self.applet = applet
        self.base_uri = base_uri
        self.base_server_label = gtk.Label("Base server URL")
        self.base_server_input = gtk.Entry(100)
        self.base_server_input.set_size_request(400,30)
      
    def build(self):
        dialog = gtk.Dialog("Configure",
                            None,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        self.base_server_input.set_text(self.base_uri)

        dialog.vbox.pack_start(self.base_server_label)
        dialog.vbox.pack_start(self.base_server_input)
        self.base_server_label.show()
        self.base_server_input.show()

        dialog.connect("response", self.ok_pressed)
        return dialog

    def ok_pressed(self, dialog, response_id):
        logging.debug("ok_pressed")
        text = self.base_server_input.get_text()
        self.applet.update_config(text)
