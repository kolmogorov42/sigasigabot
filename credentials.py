import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')

TOKEN = config.get('Credentials', 'TOKEN')
APP_URL = config.get('Credentials', 'APP_URL')
OWN_NAME = config.get('Credentials', 'OWN_NAME')
