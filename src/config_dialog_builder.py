import pygtk
pygtk.require('2.0')
import gtk
import gobject
import gnome
import gnomeapplet
import logging

class ConfigDialogBuilder:
    def __init__(self, base_uri):
        self.base_uri = base_uri

    def build(self):
        dialog = gtk.Dialog("Configure",
                            None,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        base_server_label = gtk.Label("Base server URL")
        base_server_input = gtk.Entry()
        base_server_input.set_text(self.base_uri)

        dialog.vbox.pack_start(base_server_label)
        dialog.vbox.pack_start(base_server_input)
        base_server_label.show()
        base_server_input.show()
        return dialog
