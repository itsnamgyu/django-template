from django.core import mail
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from modern_email import settings


def get_context():
    context = dict()
    context['logo_max_length'] = settings.LOGO_MAX_LENGTH
    context['organization'] = settings.ORGANIZATION_NAME
    context['address_line_1'] = settings.ADDRESS_LINE_1
    context['address_line_2'] = settings.ADDRESS_LINE_2
    context['support_email'] = settings.SUPPORT_EMAIL
    return context


def send_mail(subject,
              message,
              from_email,
              recipient_list,
              html_message=None,
              **kwargs):
    context = get_context()
    if html_message:
        context['content'] = mark_safe(html_message)
    else:
        context['content'] = message

    templated_message = render_to_string('modern_email/default_template.html',
                                         context=context)
    mail.send_mail(subject,
                   message,
                   from_email,
                   recipient_list,
                   html_message=templated_message,
                   **kwargs)