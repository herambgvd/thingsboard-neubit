from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("summary/", views.summary_dashboard, name="summary_dashboard"),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
    path("api/user-signups/", views.UserSignupStatsView.as_view(), name="user_signups_api"),
]
