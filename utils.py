import json
from typing import Dict

import psycopg2
import ast
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests.exceptions as exception


def remove_token(database: Dict) -> None:
    """
    removing token, party id from given database
    database: database details
    """
    db = psycopg2.connect(host=database["host"],
                          database=database["database_name"],
                          port=database["port"],
                          user=database["username"],
                          password=database["password"])
    cursor = db.cursor()
    cursor.execute("SELECT id,data FROM events where type_name='user'")
    for row_number, record in cursor.fetchall():
        record = ast.literal_eval(record)
        try:
            del record["metadata"]['user_details']['token']
            del record["metadata"]['user_details']['user_details']['partyId']
            del record["parse_data"]["metadata"]['user_details']['token']
            del record["parse_data"]["metadata"]['user_details']['user_details'][
                'partyId']
            record = json.dumps(record)
            with db.cursor() as cur_update:
                cur_update.execute('update events set data = %s where id = %s',
                                   (str(record), row_number))
        except KeyError:
            # token and partyid are already deleted
            pass
    db.commit()


def mail(url, bot_name, sender, password, receiver):
    """
    url: endpoint of chatbot
    bot_name: chatbot name
    sender: sender email address
    password: sender password
    receiver: Receiver email address
    """
    body = None
    message = MIMEMultipart()
    message["From"] = sender
    message["Subject"] = "{} is down".format(bot_name)
    try:
        response = requests.get(url, verify=False)
        status_code = response.status_code
        print("status code", status_code)
        if status_code != 200:
            body = "{} rasa server is down with status code:{}.".format(
                bot_name, status_code)
    except (ConnectionRefusedError, exception.ConnectionError):
        print("server is down")
        # Add body to email
        body = f"{bot_name} rasa server is down due to refused connection."
    if body:
        message.attach(MIMEText(body, "plain"))
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(sender, password)
        for receive in receiver:
            message["To"] = receive
            s.sendmail(sender, receive, message.as_string())
        s.quit()
