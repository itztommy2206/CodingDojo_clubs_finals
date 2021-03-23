from django.urls import path
from . import views

urlpatterns = [
    path("", views.firstPage),
    path("registration_process", views.register),
    path("login_process", views.login),
    path("logout", views.logout),
    path("groups", views.dashboard),
    path("create_org", views.create_org),
    path("deleteGroup/<int:group_id>", views.deleteGroup),
    path("groups/<int:group_id>", views.displayGroup),
    path("joinGroup/<int:group_id>", views.joinGroup),
    path("leaveGroup/<int:group_id>", views.leaveGroup),
]