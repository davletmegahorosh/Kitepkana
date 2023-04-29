import smtplib
from email.mime.text import MIMEText
from string import digits
from random import shuffle
import jwt
from django.contrib.auth import authenticate
from rest_framework import exceptions
import datetime

# send email


def send_email(user_email, verify_code=None):
    sender = 'kitepkanaproject@gmail.com'
    password = 'aajgkuzsfmiparxh'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(f'Мы отправили код для активации учетной записи : {verify_code}')
        server.sendmail(sender, user_email, msg.as_string())

        return print("The message was sent successfully")
    except Exception as error:
        return f"{error}\nCheck your login or password "


# generate code
def generate_verify_code():
    nums = ','.join(digits).split(',')
    shuffle(nums)
    new = ','.join(nums).replace(',', '')[0:6]
    return new


def user_authenticate(request, secret_key='secret', http_methods=None):
    if request.method in http_methods:
        token = request.COOKIES.get('jwt')
        if not token:
            raise exceptions.AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Unauthenticated')
        authenticate(username=payload['username'])
        if authenticate:
            return True


def decode_jwt_token(user=None, val=30):
    try:
        if user:
            payload = {
                'username': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=val),  # lifetime of token
                'iat': datetime.datetime.utcnow()  # Date of create token

            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            return token
    except Exception as error:
        print(error)
        return 'Token or user is None'
