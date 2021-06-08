from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', RedirectView.as_view(url='account/login')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('profile/', include('ticket.urls', namespace='ticket')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)