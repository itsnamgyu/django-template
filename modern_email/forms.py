from django import forms
from modern_email.mail import send_mail


class TestMailForm(forms.Form):
    sender = forms.EmailField(required=True)
    sender_name = forms.CharField(required=False)
    recipient = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(required=True)
    html_message = forms.CharField(required=False)

    def send_mail(self):
        sender = self.cleaned_data.get("sender")
        sender_name = self.cleaned_data.get("sender_name", None)
        recipient = self.cleaned_data.get("recipient")
        subject = self.cleaned_data.get("subject")
        message = self.cleaned_data.get("message")
        html_message = self.cleaned_data.get("html_message")

        send_mail(
            subject,
            message,
            sender,
            [recipient],
            from_name=sender_name,
            html_message=html_message,
        )
