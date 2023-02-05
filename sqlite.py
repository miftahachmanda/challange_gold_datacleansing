
import sqlite3
db = sqlite3.connect('database.db', check_same_thread=False)
db.text_factory = bytes
mycursor = db.cursor()
db.execute('''
CREATE TABLE tweet (tweet_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       tweet_dummy text,
                       tweet_bersih text

);
''')
db.execute('''
select * from tweet;
''')
db.commit()
