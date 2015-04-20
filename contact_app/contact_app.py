from flask import Flask, request, jsonify
from validate_email_address import validate_email
import requests
import json
import sqlite3
import logging
import logging.handlers

LOG_FILENAME = '/var/log/contact_app/error.log'

# Set up a specific logger with our desired output level
LOGGER = logging.getLogger('Contact App')
LOGGER.setLevel(logging.ERROR)

# Add the log message handler to the logger
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=1000, backupCount=5)
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)

# Your Details
MANDRILL_POST_URL = "https://mandrillapp.com/api/1.0/messages/send.json"
MANDRILL_KEY = 'XXXXXXXXXXX'
EMAIL = 'xxxxxx@xxxx.com'
NAME = 'JOHN SMITH'


@app.route('/c/test', methods=['GET'])
def test():
    LOGGER.info('Test Logging')
    return 'OKAY!'


@app.route('/c/contact_me', methods=['POST'])
def rsvp():
    """POST route handling the json request to dispatch an email.

    """
    try:
        json_data = request.get_json()
        json_data['message']['to'] = [
            {'email': EMAIL, 'name': NAME, 'type': 'to'}]
        if not validate_email(json_data['message']['from_email']):
            raise Exception('Malformed Data')
        else:
            # Log messages to sqlite3 database too...
            try:
                conn = sqlite3.connect('message_log.db')
                with conn:
                    ipaddr = request.remote_addr
                    conn.execute(
                        "INSERT INTO message_log VALUES(null, ?, ?, ?)",
                        [json_data['message']['text'], ipaddr,
                            json_data['message']['from_email']])
            except Exception, e:
                LOGGER.error('Error: Connecting to message log'
                             'database. Continuing: ' + e.message)

            # Send via Mandrill API
            json_data['key'] = MANDRILL_KEY
            headers = {'Content-type': 'application/json',
                       'Accept': 'text/plain', 'charset': 'utf8'}
            res = requests.post(MANDRILL_POST_URL,
                                data=json.dumps(json_data),
                                headers=headers)

            # Send via SMTP implementation commented below...
            '''
                import smtplib
                s = smtplib.SMTP('localhost')
                s.sendmail(EMAIL, json_data['message']['from_email'], json_data['message']['text'])
                s.quit()'''

            resp_code = res.status_code
            msg = "Request made: Trying to send... " + res.reason
            if resp_code == 400 or resp_code == 500:
                raise Exception(msg + " But can not send.")
    except Exception, e:
        LOGGER.error(e.message)
        resp_code = 400
        msg = "Bad Request: " + e.message
    message = {'message': msg}
    resp = jsonify(message)
    resp.status_code = resp_code
    return resp


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)
