from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.teams.urls import team_urlpatterns as single_team_urls
from apps.web.sitemaps import StaticViewSitemap
from apps.web.urls import team_urlpatterns as web_team_urls

sitemaps = {
    "static": StaticViewSitemap(),
}

# urls that are unique to using a team should go here
team_urlpatterns = [
    path("", include(web_team_urls)),
    path("team/", include(single_team_urls)),
    # Neubit Features URLs
    # path('settings/', include('apps.settings.urls')),
    path('infrastructure/', include('apps.infrastructure.urls')),
]

urlpatterns = [
                  # redirect Django admin login to main login page
                  path("admin/login/", RedirectView.as_view(pattern_name="account_login")),
                  path("admin/", admin.site.urls),
                  path("dashboard/", include("apps.dashboard.urls")),
                  path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
                  path("org/<slug:team_slug>/", include(team_urlpatterns)),
                  path("accounts/", include("allauth.urls")),
                  path("users/", include("apps.users.urls")),
                  path("teams/", include("apps.teams.urls")),
                  path("", include("apps.web.urls")),
                  path("support/", include("apps.support.urls")),

                  # Celery Progress
                  path("celery-progress/", include("celery_progress.urls")),
                  # auth API
                  path("api/auth/", include("apps.authentication.urls")),
                  # API docs
                  path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
                  # Swagger
                  path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
                  # Impersonation
                  path("hijack/", include("hijack.urls", namespace="hijack")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
