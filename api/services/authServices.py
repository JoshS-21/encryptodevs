import jwt
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

SECRET_KEY = 'your_secret_key'

def generate_password_reset_token(email):
    expiration = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode({'email': email, 'exp': expiration}, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token['email']
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')

def send_password_reset_email(email, token):
    reset_link = f'http://localhost:3000/reset-password?token={token}'
    msg = MIMEText(f'Your link to reset your password is {reset_link}. If you did not make this request, please ignore this email.')
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = 'your_email@example.com'
    msg['To'] = email

    s = smtplib.SMTP('smtp.example.com')
    s.login('your_email@example.com', 'your_email_password')
    s.send_message(msg)
    s.quit()
