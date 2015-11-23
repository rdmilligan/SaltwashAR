import ConfigParser

class ConfigProvider:

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("appsettings.ini")

    @property
    def animation(self):
        return self.config.getboolean("Features", "Animation")

    @property 
    def browser(self):
        return self.config.getboolean("Features", "Browser")

                 