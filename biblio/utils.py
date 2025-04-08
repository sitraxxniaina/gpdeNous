from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def envoyer_email_disponibilite_reservation(reservation):
    subject = f"Le livre '{reservation.livre.titre}' est disponible !"
    text_content = render_to_string('biblio/emails/livre_disponible.txt', {'reservation': reservation})
    html_content = render_to_string('biblio/emails/livre_disponible.html', {'reservation': reservation})
    recipient_list = [reservation.utilisateur.email]

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()