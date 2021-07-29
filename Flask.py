import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

from flask import Flask, request

app = Flask(__name__)
@app.route('/')
def hello_world():
    #value1 = request.json.get('value1', None)
    # SMTP stuff
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('ideas.alex2020@gmail.com', 'Sd2480748') #poner credenciales email: user y password

    msg = EmailMessage()
    #Cuerpo del mensaje
    msg.set_content('Alerta menos de 30CM')

    #Asunto correo
    msg['Subject'] = 'Notificacion de alerta'
    msg['From'] = 'Alex <ideas.alex2020@gmail.com>'
    msg['To'] = 'ideas.alex2020@gmail.com'

    s.send_message(msg)
    s.quit()
    return 'Email sent!'