import re

def detect_privacy_risk(message):

    risks = []

    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'\b\d{10}\b'
    credit_card_pattern = r'\b\d{16}\b'
    password_pattern = r'password\s*[:=]\s*\S+'

    if re.search(email_pattern, message):
        risks.append("Email Address")

    if re.search(phone_pattern, message):
        risks.append("Phone Number")

    if re.search(credit_card_pattern, message):
        risks.append("Credit Card Number")

    if re.search(password_pattern, message.lower()):
        risks.append("Password")

    return risks