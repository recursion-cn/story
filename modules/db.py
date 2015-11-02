import settings
import torndb

config = settings.database
db = torndb.Connection(config['host'], config['database'], config['user'], config['password'])
