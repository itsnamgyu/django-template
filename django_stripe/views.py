import logging
import stripe
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from django_stripe import settings
from django_stripe.models import *
from django_stripe import session_status

logger = logging.getLogger(__name__)


def checkout_success(request):
    try:
        id = request.GET["id"]
        next_url = request.GET["next"]
        session = CheckoutSession.objects.get(id=id)
    except (KeyError, ObjectDoesNotExist):
        raise Http404()

    if session.complete:
        if session.checkout.status == Checkout.COMPLETE:
            status = session_status.COMPLETE
        elif session.checkout.status == Checkout.MULTIPLE_CHARGES:
            status = session_status.MULTIPLE_CHARGES
        else:
            try:
                raise AssertionError("session is complete but checkout in incomplete")
            except AssertionError as e:
                logger.error(traceback.format_exc())
    else:
        status = session_status.INCOMPLETE

    redirect_url = next_url + "?status={}".format(status)
    return redirect(redirect_url)


@csrf_exempt
def checkout_completed_webhook(request):
    stripe.api_key = settings.SECRET_KEY
    endpoint_secret = settings.WEBHOOK_SIGNING_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        if CheckoutSession.verify(session.id):
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
        logger.warning(
            "invalid webhook type {} sent to checkout.session.completed endpoint".format(
                event["type"]
            )
        )
        return HttpResponse(status=400)
