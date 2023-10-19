import sqlite3
import sqlite_vss

db = sqlite3.connect('papers.db', timeout=10)
db.enable_load_extension(True)
sqlite_vss.load(db)
vss_version = db.execute('select vss_version()').fetchone()[0]
print('SQLite VSS Version: %s' % vss_version)
