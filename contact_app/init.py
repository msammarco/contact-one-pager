import os
import pwd
import sqlite3

LOG_DIR = '/var/log/contact_app/'
LOG_FILE = LOG_DIR + 'error.log'
DATABASE_FILE = 'message_log.db'

# Create logging file
if not os.path.exists(LOG_FILE):
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    log_file = os.open(LOG_FILE, os.O_RDWR | os.O_CREAT)
    gid = pwd.getpwnam('www-data').pw_gid
    uid = pwd.getpwnam('www-data').pw_uid
    os.fchown(log_file, uid, gid)

# Set up a message log database as backup for the email service
conn = sqlite3.connect(DATABASE_FILE)
with conn:
    try:
        conn.execute('''CREATE TABLE message_log
            (id INTEGER PRIMARY KEY not null, message text, ip text,
                email text)''')
        conn.execute(
            "INSERT INTO message_log VALUES(null, 'This is some text', '192.168.0.1', 'XXXXXXX@XXXXX.XXX')")
    except Exception:
        # The database has already been created.
        pass
print 'Database created with one dummy record. Log file initialized \n'
