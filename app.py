import smtplib
import ssl
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import Flask, request, url_for

app = Flask(__name__)

serializer = URLSafeTimedSerializer('Qk2dDh7bHh3vCr6gFo8bHmI5kDcJs')  # SECRET KEY


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'

    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls(context=ssl.create_default_context())
    connection.login('youremail', 'yourspecialpassword')

    email = request.form['email']
    token = serializer.dumps(email, salt='email-confirm')

    # uuid
    link = url_for('confirm_email', token=token, _external=True)

    msg = EmailMessage()
    msg.set_content(f'Your link is {link}', subtype='html')
    msg['Subject'] = 'Confirm Email'
    msg['From'] = 'youremail'
    msg['To'] = email

    connection.send_message(msg)
    connection.quit()

    return f'The email you entered is {email}. The token is {token}'


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>The token works!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
