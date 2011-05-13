
class JobImages:
    def __init__(self, config):
        self.blue_image = self.__setup_image(config.get('icon_settings', 'blue_image'))
        self.blue_anime_image = self.__setup_image(config.get('icon_settings', 'blue_anime_image'))
        self.red_anime_image = self.__setup_image(config.get('icon_settings', 'red_anime_image'))
        self.red_image = self.__setup_image(config.get('icon_settings', 'red_image'))
        self.disabled_image = self.__setup_image(config.get('icon_settings', 'disabled_image'))
        self.unknown_image = self.__setup_image(config.get('icon_settings', 'unknown_image'))

    def __setup_image(self, path):
        color_file = self.__choose_color_file(path)
        data = self.__load_image_data(color_file)
        image.set_from_pixbuf(data)
        return image

    def __choose_color_file(self, color):
        if "blue" == color:
            return self.images.blue_image
        elif "blue_anime" == color:
            return self.images.blue_anime_image
        elif "red_anime" == color:
            return self.images.red_anime_image
        elif "red" == color:
            return self.images.red_image
        elif "disabled" == color:
            return self.images.disabled_image
        else:
            logging.debug("unknown color: \""+color+"\"")
            return self.unknown_image

    def __load_image_data(self, image_file):
        return gtk.gdk.pixbuf_new_from_file_at_size(image_file, self.max_image_size, self.max_image_size)
