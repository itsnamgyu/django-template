import traceback

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.views.generic import View

from base.mixins import StaffMemberRequiredMixin, SuperUserRequiredMixin
from modern_email.forms import TestMailForm


class TestView(SuperUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        test_mail_form = TestMailForm()
        context = dict(form=test_mail_form)
        return render(self.request, 'modern_email/test.html', context=context)

    def post(self, request, *args, **kwargs):
        test_mail_form = TestMailForm(request.POST)
        message = None
        if test_mail_form.is_valid():
            try:
                test_mail_form.send_mail()
            except Exception as e:
                message = traceback.format_exc()
            else:
                message = 'Success! The email should have been sent to {}'.format(
                    test_mail_form.cleaned_data['recipient'])
        else:
            message = 'Invalid data'

        context = dict(form=test_mail_form, message=message)

        return render(self.request, 'modern_email/test.html', context=context)
