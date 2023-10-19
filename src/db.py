import sqlite3
import sqlite_vss

db = sqlite3.connect('papers.db', timeout=10)
db.enable_load_extension(True)
sqlite_vss.load(db)
vss_version = db.execute('select vss_version()').fetchone()[0]
print('SQLite VSS Version: %s' % vss_version)

# papersテーブルの作成
db.execute('''
    CREATE TABLE IF NOT EXISTS papers(
        id INTEGER PRIMARY KEY,
        title TEXT,
        abstract TEXT,
        summary TEXT,
        url TEXT,
        created_at DATETIME
    );
''')

# vss_paperテーブルの作成
db.execute('''
    CREATE VIRTUAL TABLE IF NOT EXISTS vss_papers USING vss0(
        summary_embedding(1536)
    );
''')
