import ConfigParser

def prase_config(section, option):
    config = ConfigParser.ConfigParser()
    config.read('./weblogic.cfg')
    return config.get(section, option)
