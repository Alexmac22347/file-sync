import ConfigParser

CONFIGFILENAME = 'config.ini'


# TODO: Make filename passable from command line
class config:

    def __init__(self):
        self.configParser = ConfigParser.SafeConfigParser()
        self.values = {}
        try:
            self.configParser.read(CONFIGFILENAME)
        except IOError:
            open('{}'.format(CONFIGFILENAME), 'w')
            self.configParser.read(open(CONFIGFILENAME))

    def readConfig(self):
        # If the config is empty we raise an exception.
        # Another class will handle the initialization
        if not self.configParser.sections():
            raise NoConfigException

        for section in self.configParser.sections():
            self.values[section] = {}
            for option in self.configParser.options(section):
                self.values[section][option] = self.configParser.get(section, option)


    def writeConfig(self):
        for section in self.values.keys():
            try:
                self.configParser.add_section(section)
            except ConfigParser.DuplicateSectionError:
                pass
            for key in self.values[section]:
                self.configParser.set(section, key, self.values[section][key])

        with open(CONFIGFILENAME, 'w') as f:
            self.configParser.write(f)


class NoConfigException(Exception):
    pass

globalConfig = config()
