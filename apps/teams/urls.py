from django.urls import path
from rest_framework import routers

from . import views

app_name = "teams"

urlpatterns = [
    path("manage/", views.manage_teams, name="manage_teams"),
    path("create/", views.create_team, name="create_team"),
    # invitation acceptance views
    path("invitation/<slug:invitation_id>/", views.accept_invitation, name="accept_invitation"),
    path("invitation/<slug:invitation_id>/signup/", views.SignupAfterInvite.as_view(), name="signup_after_invite"),
]

team_urlpatterns = (
    [
        path("", views.manage_team, name="manage_team"),
        path("delete", views.delete_team, name="delete_team"),
        path("members/<int:membership_id>/", views.team_membership_details, name="team_membership_details"),
        path("members/<int:membership_id>/remove/", views.remove_team_membership, name="remove_team_membership"),
        path("invite/<slug:invitation_id>/", views.resend_invitation, name="resend_invitation"),
        path("invite/", views.send_invitation_view, name="send_invitation"),
        path("invite/cancel/<slug:invitation_id>/", views.cancel_invitation_view, name="cancel_invitation"),
    ],
    "single_team",
)

# DRF config for API views (required for React Teams, implementation, optional otherwise)
router = routers.DefaultRouter()
router.register("api/teams", views.TeamViewSet)
urlpatterns += router.urls

single_team_router = routers.DefaultRouter()
single_team_router.register("api/invitations", views.InvitationViewSet)
team_urlpatterns[0].extend(single_team_router.urls)
