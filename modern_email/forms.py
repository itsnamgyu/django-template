from django import forms
from modern_email.mail import send_mail


class TestMailForm(forms.Form):
    sender = forms.EmailField(required=True)
    recipient = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(required=True)
    html_message = forms.CharField(required=False)

    def send_mail(self):
        sender = self.cleaned_data.get('sender')
        recipient = self.cleaned_data.get('recipient')
        subject = self.cleaned_data.get('subject')
        message = self.cleaned_data.get('message')
        html_message = self.cleaned_data.get('html_message')

        print(' sender '.center(100, '-'))
        print(sender)
        print(' recipient '.center(100, '-'))
        print(recipient)
        print(' subject '.center(100, '-'))
        print(subject)
        print(' message '.center(100, '-'))
        print(message)
        print(' html_message '.center(100, '-'))
        print(html_message)

        send_mail(subject, message, sender, [recipient], html_message)
