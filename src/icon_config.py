
class IconConfig:
    def __init__(self, config):
        self.blue = config.get('icon_settings', 'blue')
        self.blue_anim = config.get('icon_settings', 'blue_anim')
        self.red_anim = config.get('icon_settings', 'red_anim')
        self.red = config.get('icon_settings', 'red')
        self.disabled = config.get('icon_settings', 'disabled')
        self.unknown = config.get('icon_settings', 'unknown')
