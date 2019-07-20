# ModernEmail

A simple app that makes it easy to send decent looking emails with your logo on it.

## Setup

This app uses your Django [email backend](https://docs.djangoproject.com/en/2.2/topics/email/#email-backends) to send emails–so make sure to set it up first. If you are setting an email backend for the first time, [Amazon SES](https://aws.amazon.com/ses/) and [this](https://github.com/django-ses/django-ses) adapter module is a great place to start for production email.

Next, put these settings in your `settings.py`.

```
MODERN_EMAIL_LOGO_IMAGE = 'img/logo.png'
MODERN_EMAIL_STATIC_HOST = 'http://deploymenturl.com'
MODERN_EMAIL_CUSTOM_TEMPLATE_FILE = 'email_template.html'
MODERN_EMAIL_LOGO_MAX_LENGTH = 100
MODERN_EMAIL_SUPPORT_EMAIL = 'support@deploymenturl.com'
MODERN_EMAIL_ADDRESS_LINE_1 = '1070 E Arques Ave'
MODERN_EMAIL_ADDRESS_LINE_2 = 'Sunnyvale, CA 94085'
MODERN_EMAIL_ORGANIZATION_NAME = 'My Company'
MODERN_EMAIL_COPYRIGHT_START_YEAR = '2019'
```

- `MODERN_EMAIL_LOGO_IMAGE`: your logo image file. The same string that you would use in `{% static 'here' %}`.
- `MODERN_EMAIL_STATIC_HOST`: the domain where you actually host this project. This is required because images can only be inserted in emails via absolute urls `http://deploymenturl.com/static/logo.png`. This is not required if your `STATIC_URL` is an absolute url. This would usually be the case if you use a cloud service such as Amazon S3 to serve static files.
- `MODERN_EMAIL_CUSTOM_TEMPLATE`: you can override the default template by providing your own template file. The same string that you would use in `return render('here.html')`. Not yet supported.
- `MODERN_EMAIL_LOGO_MAX_LENGTH`: the max width and max height of your logo displayed in the email, in pixels. Default value is 100.

### Requirements

- [`django-boostrap4`](https://readthedocs.org/projects/django-bootstrap4/)

## Send Mail!

### `modern_email.send_mail`

Sends a templated html email using the [`django.core.mail.send_mail`](https://docs.djangoproject.com/en/2.2/topics/email/#send-mail) method internally. You can insert either a plain string (`message`) or html string (`html_message`) to insert into the template.

```python
from modern_email import send_mail

modern_email.send_mail(
    subject,
    message,
    from_email,
    recipient_list,
    html_message=None,
    **kwargs)
```

- `subject`: A string.
- `message`: A string. This will be inserted in the template by default.
- `from_email`: A string.
- `recipient_list`: A list of strings, each an email address. Each member of recipient_list will see the other recipients in the “To:” field of the email message.
- `html_message`: An html string. If specified, this will be inserted in the template instead of `message`. Unlike Django's `send mail`, omitting this field will still result in a multipart/alternative email with `message` as the text/plain content type and the \_templated\* `message` as the text/html content type.

#### \*\*kwargs

These are keyword arguments to Django's [`send_mail`](https://docs.djangoproject.com/en/2.2/topics/email/#send-mail) function, that are not handled by the app.

- fail_silently: A boolean. When it’s False, send_mail() will raise an smtplib.SMTPException if an error occurs. See the smtplib docs for a list of possible exceptions, all of which are subclasses of SMTPException.
- auth_user: The optional username to use to authenticate to the SMTP server. If this isn’t provided, Django will use the value of the EMAIL_HOST_USER setting.
- auth_password: The optional password to use to authenticate to the SMTP server. If this isn’t provided, Django will use the value of the EMAIL_HOST_PASSWORD setting.
- connection: The optional email backend to use to send the mail. If unspecified, an instance of the default backend will be used. See the documentation on Email backends for more details.

## Manual Testing

Go to `modern_email:test` (`/modern-email/test`) as a superuser to send a test email.
