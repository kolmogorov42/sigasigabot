import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')

TOKEN = config.get('Credentials', 'TOKEN')
OWN_NAME = config.get('Credentials', 'OWN_NAME')
