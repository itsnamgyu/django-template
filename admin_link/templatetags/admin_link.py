"""Based on the [Django template tag for admin urls](django/django/contrib/admin/templatetags/admin_urls.py).
"""

from boto.cloudfront import logging
from django import template
from django.template.loader import render_to_string
from django.urls import reverse

register = template.Library()

ACTIONS = ("changelist", "add", "change", "delete")


@register.simple_tag(takes_context=True)
def admin_link_url(context, instance, action: str):
    user = context.request.user
    if not user.is_authenticated:
        return None

    if action not in ACTIONS:
        raise ValueError(
            "`action` must be one of {}. Value provided is `{}`.".format(
                ACTIONS, action
            )
        )

    try:
        app = instance._meta.app_label
        model = instance._meta.model_name
    except AttributeError:
        return None

    if not user.has_perm("{}.{}_{}".format(app, action, model)):
        return None

    url_name = "admin:%s_%s_%s" % (app, model, action)

    if action in ("change", "delete"):
        args = (instance.pk,)
    else:
        args = ()

    url = reverse(
        url_name, args=args, current_app=context.request.resolver_match.app_name
    )
    full_url = "{}?admin_link_redirect={}".format(url, context.request.get_full_path())

    return full_url


@register.simple_tag(takes_context=True)
def admin_link(context, instance, action: str, label: str = None):
    url = admin_link_url(context, instance, action)

    try:
        app_label = instance._meta.app_label.replace("_", " ")
        model_name = instance._meta.model_name.replace("_", " ")
    except AttributeError:
        return ""

    local_context = dict(
        url=url, label=label, app_label=app_label, model_name=model_name
    )

    if url:
        return render_to_string(
            "admin_link/{}.html".format(action), context=local_context
        )
    else:
        return ""
