from django.urls import path

from . import views

from .views import (
    property_meetings,
    edit_developer,
    edit_architect,
    edit_engineer,
    edit_project,
    edit_meeting,
)


urlpatterns = [

    # =========================================================
    # PROPERTY HOME
    # =========================================================

    path(
        "",
        views.index,
        name="properties",
    ),

    path(
        "residential/",
        views.residential_projects,
        name="residential_projects",
    ),

    path(
        "commercial/",
        views.commercial_projects,
        name="commercial_projects",
    ),

    path(
        "search/",
        views.search_projects,
        name="search_projects",
    ),

    path(
        "submit-enquiry/<int:id>/",
        views.submit_enquiry,
        name="submit_enquiry",
    ),

    path(
        "thank-you/",
        views.thank_you,
        name="thank_you",
    ),

    path(
        "api/search-suggestions/",
        views.search_suggestions,
        name="search_suggestions",
    ),


    # =========================================================
    # PROPERTY MEETINGS
    # =========================================================

    path(
        "dashboard/meeting/property/",
        property_meetings,
        name="property_meetings",
    ),


    # =========================================================
    # DEVELOPER EDIT
    # =========================================================

    path(
        "dashboard/meeting/developer/<str:developer_id>/edit/",
        edit_developer,
        name="edit_developer",
    ),


    # =========================================================
    # ARCHITECT EDIT
    # =========================================================

    path(
        "dashboard/meeting/architect/<str:architect_id>/edit/",
        edit_architect,
        name="edit_architect",
    ),


    # =========================================================
    # ENGINEER EDIT
    # =========================================================

    path(
        "dashboard/meeting/engineer/<str:engineer_id>/edit/",
        edit_engineer,
        name="edit_engineer",
    ),


    # =========================================================
    # PROJECT EDIT
    # =========================================================

    path(
        "dashboard/meeting/project/<str:project_id>/edit/",
        edit_project,
        name="edit_project",
    ),


    # =========================================================
    # MEETING EDIT
    # =========================================================

    path(
        "dashboard/meeting/<str:meeting_id>/edit/",
        edit_meeting,
        name="edit_meeting",
    ),


    # =========================================================
    # PROJECT DETAILS
    # =========================================================

    path(
        "<int:id>/<slug:slug>/",
        views.project_details,
        name="project_details",
    ),
]