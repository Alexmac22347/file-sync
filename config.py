import ConfigParser

CONFIGFILENAME = 'config.ini'


class config:
    """This class will read and write from the config.ini file. It is
    needed to remember user settings, and to remeber a list of locally and
    remotely stored files"""

    def __init__(self):
        """Create the config.ini file and read from it, or just
        read from it if it already exists"""

        self.configParser = ConfigParser.SafeConfigParser()
        self.values = {}
        try:
            self.configParser.read(CONFIGFILENAME)
        except IOError:
            open('{}'.format(CONFIGFILENAME), 'w')
            self.configParser.read(open(CONFIGFILENAME))

    def readConfig(self):
        """update self.values to reflect what is in the
        config.ini file"""

        # If the config is empty we raise an exception.
        # Another class will handle the initialization
        if not self.configParser.sections():
            raise NoConfigException

        for section in self.configParser.sections():
            self.values[section] = {}
            for option in self.configParser.options(section):
                self.values[section][
                    option] = self.configParser.get(section, option)

    def writeConfig(self):
        """Write our local values to the config.ini file."""

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
    """This exception is used for when no config.ini file is found"""
    pass
