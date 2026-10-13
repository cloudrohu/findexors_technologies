from django.urls import path

from . import views

from apps.properties.views import (
    edit_developer,
    edit_architect,
    edit_engineer,
    edit_project,
    edit_meeting,
)


urlpatterns = [

    # =========================================================
    # PROPERTY MEETINGS
    # =========================================================

    path(
        "property/",
        views.property_meetings,
        name="property_meetings",
    ),


    # =========================================================
    # DEVELOPER EDIT
    # =========================================================

    path(
        "developer/<str:developer_id>/edit/",
        edit_developer,
        name="edit_developer",
    ),


    # =========================================================
    # ARCHITECT EDIT
    # =========================================================

    path(
        "architect/<str:architect_id>/edit/",
        edit_architect,
        name="edit_architect",
    ),


    # =========================================================
    # ENGINEER EDIT
    # =========================================================

    path(
        "engineer/<str:engineer_id>/edit/",
        edit_engineer,
        name="edit_engineer",
    ),


    # =========================================================
    # PROJECT EDIT
    # =========================================================

    path(
        "project/<str:project_id>/edit/",
        edit_project,
        name="edit_project",
    ),


    # =========================================================
    # MEETING EDIT
    # =========================================================

    path(
        "<str:meeting_id>/edit/",
        edit_meeting,
        name="edit_meeting",
    ),
]