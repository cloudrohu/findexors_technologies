from django.urls import path

from . import views

from apps.properties import views as property_views
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


# =========================================================
    # PROPERTIES
    # =========================================================

    path(
        "dashboard/properties/projects/",
        property_views.property_projects,
        name="property_projects",
    ),

    path(
        "dashboard/properties/developers/",
        property_views.property_developers,
        name="property_developers",
    ),

    path(
        "dashboard/properties/architects/",
        property_views.property_architects,
        name="property_architects",
    ),

    path(
        "dashboard/properties/engineers/",
        property_views.property_engineers,
        name="property_engineers",
    ),

    path(
        "dashboard/properties/project/<str:project_id>/",
        property_views.property_project_detail,
        name="property_project_detail"
    ),

]