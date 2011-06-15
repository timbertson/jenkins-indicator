class IconConfig:
    def __init__(self, config):
        self.blue = config.get('icon_settings', 'blue')
        self.blue_anime = config.get('icon_settings', 'blue_anime')
        self.red_anime = config.get('icon_settings', 'red_anime')
        self.red = config.get('icon_settings', 'red')
        self.disabled = config.get('icon_settings', 'disabled')
        self.unknown = config.get('icon_settings', 'unknown')
        self.aborted = config.get('icon_settings', 'aborted')
