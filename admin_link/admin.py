from django.contrib import admin
from django.http import HttpResponseRedirect


class ModelAdmin(admin.ModelAdmin):
    """Use this ModelAdmin base class to enabled redirect-backs for admin
    links. When you use an admin link to change a model registered to the
    Django admin using this class, you will be automatically redirected back
    to the original page, containing the admin link

    TODO improve this docstring.
    """

    def _response_post_save(self, request, obj):
        redirect = request.GET.get("admin_link_redirect")
        if redirect:
            return HttpResponseRedirect(redirect)
        else:
            return super(ModelAdmin, self)._response_post_save(request, obj)
