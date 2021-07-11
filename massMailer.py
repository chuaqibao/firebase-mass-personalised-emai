from pyrebase import pyrebase

import random
import string

import smtplib, csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

config = {
"apiKey": "your-firebase-api-key",
"authDomain": "your-firebase-auth-domain",
"databaseURL": "your-firebase-database-url",
"storageBucket": "your-firebase-storage-bucket",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def createUser(email, password):
    print("Username: " + email)
    print("Password: " + password)
    auth.create_user_with_email_and_password(email, password)

def generatePassword():
    length = 11
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    num = string.digits

    all = lower + upper + num
    temp = random.sample(all, length)

    password = "".join(temp)
    return password

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        mail_content = file.read()
        return mail_content

def sendMail():
    mail_body = read_template('test.txt')

    print("Login")
    email = input("Enter your gmail: ")
    password = input("Enter your password: ")

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(email, password)

    with open("test.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            user_email = row[10].strip()
            user_password = generatePassword()

            createUser(user_email, user_password)

            msg = MIMEMultipart()
            message = mail_body.format(PERSON=row[7].strip().upper(), USERNAME=user_email, PASSWORD=user_password)
            print(message)

            msg['From'] = email
            msg['To'] = row[10]
            msg['Subject'] = '[Confirmation] Test Email Send'

            msg.attach(MIMEText(message, 'html'))

            s.send_message(msg)
            del msg

    s.quit()

sendMail()

uids = []

