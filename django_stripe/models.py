import logging
import uuid
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import stripe
from django_stripe import settings

from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class Checkout(models.Model):
    COMPLETE = "CO"
    INCOMPLETE = "IC"
    MULTIPLE_CHARGES = "MC"
    status_choices = (
        (COMPLETE, "Complete"),
        (INCOMPLETE, "Incomplete"),
        (MULTIPLE_CHARGES, "Multiple Charges"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_status_modified = models.DateTimeField(
        _("date status modified"), auto_now=True
    )
    status = models.CharField(_("status"), max_length=2, choices=status_choices)
    amount = models.IntegerField(_("price amount"))
    currency = models.CharField(_("currency"), max_length=3, default="usd")
    quantity = models.IntegerField(_("quantity"), default=1)

    name = models.TextField(_("name"))
    description = models.TextField(_("description"), null=True, blank=True)
    key = models.CharField(_("key"), max_length=256, null=True, blank=True)
    prefilled_email = models.EmailField(_("prefilled email"), null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["key"])]

    def get_checkout_session(
        self, cancel_url, success_url, reuse_threshold=datetime.timedelta(hours=12)
    ):
        session = None
        try:
            latest_session = self.checkout_set.latest()
            reuse = True
            reuse = reuse and latest_session.cancel_url == cancel_url
            reuse = reuse and latest_session.success_url == success_url
            expired = latest_session.date_created < timezone.now() - reuse_threshold
            reuse = reuse and not expired
            if reuse:
                session = latest_session
        except ObjectDoesNotExist:
            pass

        if not session:
            session = CheckoutSession.init_session(self, cancel_url, success_url)

        return session


class CheckoutSession(models.Model):
    checkout = models.ForeignKey(
        Checkout, on_delete=models.SET_NULL, related_name="checkout_set", null=True
    )
    session_id = models.CharField(
        _("stripe checkout id"), max_length=128, null=True, blank=True
    )
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_completed = models.DateTimeField(_("date completed"), null=True, blank=True)
    completed = models.BooleanField(_("completed"), default=False)

    cancel_url = models.URLField(_("cancel url"))
    success_url = models.URLField(_("success_url"))

    class Meta:
        indexes = [
            models.Index(fields=["session_id", "date_created"]),
            models.Index(fields=["date_created"]),
        ]

    @staticmethod
    def verify(session_id):
        session = CheckoutSession.objects.filter(session_id=session_id).first()
        if session:
            if session.completed:
                logger.warning("duplicate verification of checkout session ")
            else:
                session.completed = True
                checkout = session.checkout
                if checkout.status == Checkout.INCOMPLETE:
                    checkout.status = Checkout.COMPLETE
                elif checkout.status == Checkout.COMPLETE:
                    checkout.status = Checkout.MULTIPLE_CHARGES
                checkout.save()
            return True
        else:
            return False

    @staticmethod
    def init_session(checkout: Checkout, cancel_url, success_url):
        session = CheckoutSession(checkout=checkout)

        stripe.api_key = settings.SECRET_KEY

        success_url = success_url + "?id={}&next={}".format(checkout.id, success_url)
        stripe_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                dict(
                    name=payment.name,
                    description=payment.description,
                    amount=payment.amount,
                    currency=payment.currency,
                    quantity=payment.quantity,
                )
            ],
            success_url=success_url,
            cancel_url=cancel_url,
        )
        session.id = stripe_session.id
        session.save()

        return session
