from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

DOMAIN = "phytorganic.net"


def notifier(**kwargs):
    action = kwargs.get("action")
    e_subject = kwargs.get("e_subject")
    e_sender = kwargs.get("e_sender", "info")
    e_receiver = kwargs.get("e_receiver")
    e_context = kwargs.get("e_context")

    text_content = get_template('notify/{}.txt'.format(action))
    html_content = get_template('notify/{}.html'.format(action))

    subject, from_email, to = e_subject, "{0}@{1}".format(e_sender, DOMAIN), e_receiver
    text_content = text_content.render(e_context)
    html_content = html_content.render(e_context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
