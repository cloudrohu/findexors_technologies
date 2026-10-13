from django.urls import path

from . import views


urlpatterns = [

    # Dashboard
    path(
        "dashboard/",
        views.dashboard_index,
        name="dashboard",
    ),

    # Login
    path(
        "login/",
        views.dashboard_login,
        name="dashboard_login",
    ),

    # Logout
    path(
        "logout/",
        views.dashboard_logout,
        name="dashboard_logout",
    ),

]