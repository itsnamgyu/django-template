import datetime

from django.core import mail
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from modern_email import settings


def get_context():
    context = dict()
    context["logo_max_length"] = settings.LOGO_MAX_LENGTH
    context["organization"] = settings.ORGANIZATION_NAME
    context["address_line_1"] = settings.ADDRESS_LINE_1
    context["address_line_2"] = settings.ADDRESS_LINE_2
    context["support_email"] = settings.SUPPORT_EMAIL

    end = str(datetime.datetime.now().year)
    if settings.COPYRIGHT_START_YEAR:
        start = str(settings.COPYRIGHT_START_YEAR)
    else:
        start = end

    if start == end:
        year_range = start
    else:
        year_range = "{}-{}".format(start, end)
    context["copyright_year_range"] = year_range

    return context


def send_mail(
    subject,
    message,
    from_email,
    recipient_list,
    from_name=None,
    html_message=None,
    **kwargs
):
    context = get_context()
    if html_message:
        context["content"] = mark_safe(html_message)
    else:
        context["content"] = message

    templated_message = render_to_string(
        "modern_email/default_template.html", context=context
    )

    if from_name:
        named_from_email = '"{}" <{}>'.format(from_name, from_email)
    else:
        named_from_email = from_email

    mail.send_mail(
        subject,
        message,
        named_from_email,
        recipient_list,
        html_message=templated_message,
        **kwargs
    )
