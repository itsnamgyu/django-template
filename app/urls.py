"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from app.settings import MODERN_EMAIL_ENABLED, STRIPE_ENABLED

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("example.urls")),
    path("accounts/", include("allauth.urls")),
    path("ckeditor_uploader/", include("ckeditor_uploader.urls")),
    # path('', include('social_django.urls', namespace='social')),  # enable for social login
]

if settings.MODERN_EMAIL_ENABLED:
    urlpatterns.append(path("modern-email/", include("modern_email.urls")))

if settings.STRIPE_ENABLED:
    urlpatterns.append(path("stripe/", include("django_stripe.urls")))

if settings.DT_STRIPE_ENABLED:
    urlpatterns.append(path("dt-stripe/", include("dt_stripe.urls")))

if settings.DT_CONTENT_ENABLED:
    urlpatterns.append(path("dt-content/", include("dt_content.urls")))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns.extend([path("__debug__/", include(debug_toolbar.urls))])

