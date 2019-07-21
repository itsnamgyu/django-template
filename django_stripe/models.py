import uuid
from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Checkout(models.Model):
    COMPLETE = 'CO'
    INCOMPLETE = 'IC'
    MULTI_CHARGE = 'MC'
    status_choices = ((COMPLETE, 'Complete'), (INCOMPLETE, 'Incomplete'),
                      (MULTI_CHARGE, 'Multiple Charges'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_status_modified = models.DateTimeField(_('date status modified'),
                                                auto_now=True)
    status = models.CharField(_('status'),
                              max_length=2,
                              choices=status_choices)

    description = models.TextField(_('description'), null=True, blank=True)
    key = models.CharField(_('key'), max_length=256, null=True, blank=True)
    prefilled_email = models.EmailField(_('prefilled email'),
                                        null=True,
                                        blank=True)

    def get_checkout(self,
                     cancel_url,
                     success_url,
                     reuse_threshold=datetime.timedelta(hours=12)):
        raise NotImplementedError()


class CheckoutSession(models.Model):
    payment = models.ForeignKey(Checkout,
                                on_delete=models.SET_NULL,
                                related_name='checkout_set')
    session_id = models.CharField(_('stripe checkout id'),
                                  null=True,
                                  blank=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_completed = models.DateTimeField(_('date completed'),
                                          null=True,
                                          blank=True)
    completed = models.BooleanField(_('completed'), default=False)

    cancel_url = models.URLField(_('cancel url'))
    success_url = models.URLField(_('success_url'))
