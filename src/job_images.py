import logging
import gtk
from icon_config import IconConfig

class JobImages:
    def __init__(self, config, max_image_size):
        self.icon_config = IconConfig(config)
        self.max_image_size = max_image_size

        self.blue = self.__setup_image('blue')
        self.blue_anime = self.__setup_image('blue_anime')
        self.red_anime = self.__setup_image('red_anime')
        self.red = self.__setup_image('red')
        self.disabled = self.__setup_image('disabled')
        self.unknown = self.__setup_image('unknown')

    def get(self, color):
        if "blue" == color:
            return self.__setup_image('blue')
            #return self.blue
        elif "blue_anime" == color:
            return self.__setup_image('blue_anime')
            #return self.blue_anime
        elif "red_anime" == color:
            return self.__setup_image('red_anime')
            #return self.red_anime
        elif "red" == color:
            return self.__setup_image('red')
            #return self.red
        elif "disabled" == color:
            return self.__setup_image('disabled')
            #return self.disabled
        elif "unknown" == color:
            return self.__setup_image('unknown')
            #return self.unknown
        else:
            logging.debug("unknown color: "+color)
            return None

    def __setup_image(self, path):
        color_file = self.__choose_color_file(path)
        data = self.__load_image_data(color_file)
        image = gtk.Image()
        image.set_from_pixbuf(data)
        return image

    def __choose_color_file(self, color):
        if "blue" == color:
            return self.icon_config.blue
        elif "blue_anime" == color:
            return self.icon_config.blue_anime
        elif "red_anime" == color:
            return self.icon_config.red_anime
        elif "red" == color:
            return self.icon_config.red
        elif "disabled" == color:
            return self.icon_config.disabled
        elif "unknown" == color:
            return self.icon_config.unknown
        else:
            logging.debug("unknown color: "+color)
            return None

    def __load_image_data(self, image_file):
        return gtk.gdk.pixbuf_new_from_file_at_size(image_file, self.max_image_size, self.max_image_size)
