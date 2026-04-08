import os
import smtplib
from email.mime.text import MIMEText

from dotenv import find_dotenv, load_dotenv
from form import Contact

load_dotenv(find_dotenv())

sender = os.environ.get("SMTP_USER")
password = os.environ.get("SMTP_PASSWORD")

subject = "Merci pour votre message ✨"

body = (
    "Bonjour {first_name},\n\n"
    "Merci pour votre message 💌\n"
    "Je l’ai bien reçu et je reviens vers vous très rapidement.\n\n"
    "Que ce soit pour une question, une envie de voyage ou simplement en savoir plus, "
    "je serai ravie d’échanger avec vous.\n\n"
    "À très bientôt,\n"
    "Aloïs – Numa Travel ✈️"
)


def confirmation_email(first_name: str, user_email: str) -> None:

    msg = MIMEText(body.format(first_name=first_name))
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = user_email

    with smtplib.SMTP_SSL(
        os.environ.get("SMTP_HOST"), os.environ.get("SMTP_PORT")
    ) as server:
        server.login(sender, password)
        server.send_message(msg)


def send_email_to_admin(form_data: Contact) -> None:

    admin_email = sender
    subject_admin = "Nouveau message de contact reçu"
    body_admin = (
        f"Vous avez reçu un nouveau message de contact :\n\n"
        f"Nom : {form_data.first_name} Prénom : {form_data.last_name}\n"
        f"Email : {form_data.email}\n"
        f"Message : {form_data.message}\n"
        f"Phone : {form_data.phone if form_data.phone else 'N/A'}"
    )

    msg_admin = MIMEText(body_admin)
    msg_admin["Subject"] = subject_admin
    msg_admin["From"] = sender
    msg_admin["To"] = admin_email

    with smtplib.SMTP_SSL(
        os.environ.get("SMTP_HOST"), os.environ.get("SMTP_PORT")
    ) as server:
        server.login(sender, password)
        server.send_message(msg_admin)
