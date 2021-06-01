from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from messenger.views import signup


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy('friends'))),
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", signup, name='signup'),
    path("messenger/", include('messenger.urls'))
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
