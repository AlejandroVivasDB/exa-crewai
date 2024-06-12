#!/usr/bin/env python
from datetime import datetime
from newsletter_gen.crew import NewsletterGenCrew
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

def load_html_template(): 
    with open('src/newsletter_gen/config/newsletter_template.html', 'r') as file:
        html_template = file.read()
        
    return html_template

def send_email(html_content, to_email):
    # Configura los parámetros del correo
    from_email = "tu_email@ejemplo.com"
    subject = "Weekly Newsletter"

    # Crea el mensaje de correo
    msg = MIMEMultipart('related')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Adjunta el contenido HTML
    msg.attach(MIMEText(html_content, 'html'))

    # Envía el correo
    with smtplib.SMTP('smtp.ejemplo.com', 587) as server:
        server.starttls()
        server.login(from_email, 'tu_contraseña')
        server.sendmail(from_email, to_email, msg.as_string())


def run():
    # Reemplaza con tus inputs, interpolará automáticamente cualquier información de tareas y agentes
    topic = input('Enter the topic for your newsletter: ')
    personal_message = input('Enter a personal message for your newsletter: ')
    inputs = {
        'topic': topic,
        'personal_message': personal_message,
        'html_template': load_html_template()
    }
    
    newsletter_crew = NewsletterGenCrew()
    newsletter_crew.crew().kickoff(inputs=inputs)
    
    # Asegurar la creación del directorio logs
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Generar el nombre del archivo basado en la fecha y el tema
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_filename = f"logs/{date_str}_newsletter_task.html"
    
    # Asume que la tarea de la newsletter genera un archivo HTML de salida con este nombre
    with open(output_filename, 'r') as file:
        html_content = file.read()
    
    send_email(html_content, "alejandro.vivas@dualbootpartners.com")

if __name__ == "__main__":
    run()