# credit : https://realpython.com/python-send-email/

import smtplib, ssl
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict

# credentials
sender_email = "cse101sectionc@gmail.com"
password = input("Password: ")

# list of emails to send to
# list should be im the emails text file
receiver_emails = []
with open('emails', 'r') as file:
    receiver_emails = file.read().splitlines()

# problem bank
problems = []
with open('problems', 'r') as file:
    problems = file.read().splitlines()
n = len(problems)

# randomly assign to each problem
assigned = [[] for _ in range(n)]
random.shuffle(receiver_emails)
i = 0  # would error if no problems at all
while receiver_emails:
    assigned[i].append(receiver_emails.pop())
    i = (i + 1) % n

print("\nAssigned as follows: ")
for i in range(n):
    print('{} : {}'.format(problems[i], assigned[i]))

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    for i in range(n):
        for receiver_email in assigned[i]:
            # generate message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Your Quiz Problem for Section C"
            message["From"] = sender_email
            message["To"] = receiver_email
            text = "Hi\nYour problem for the quiz is: {}".format(problems[i])
            html = "<html><p>Hi,</p><p>Your problem for the quiz is: <span style=\"color: red;font-weight: bold\">{}</span></p></html>".format(
                problems[i])
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            server.sendmail(sender_email, receiver_email, message.as_string())
