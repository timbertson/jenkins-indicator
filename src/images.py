
class Images:
    def __init__(self, config):
        self.blue_image = config.get('icon_settings', 'blue_image')
        self.blue_anime_image = config.get('icon_settings', 'blue_anime_image')
        self.red_anime_image = config.get('icon_settings', 'red_anime_image')
        self.red_image = config.get('icon_settings', 'red_image')
        self.disabled_image = config.get('icon_settings', 'disabled_image')
        self.unknown_image = config.get('icon_settings', 'unknown_image')
