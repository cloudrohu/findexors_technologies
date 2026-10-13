from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from apps.properties.models import Meeting


@login_required
def property_meetings(request):

    # =========================================================
    # DATE
    # =========================================================
    today = timezone.localdate()
    tomorrow = today + timezone.timedelta(days=1)


    # =========================================================
    # ALL MEETINGS
    # =========================================================
    meetings = (
        Meeting.objects
        .select_related(
            "developer",
            "architect",
            "engineer",
            "project",
            "assigned_to",
        )
        .all()
        .order_by("meeting_date")
    )


    # =========================================================
    # NOT MANAGE QUERY
    # =========================================================
    not_manage_q = (
        Q(
            meeting_date__date__lt=today,
            project__calling_status__in=[
                "Meeting",
                "Meeting_FollowUp",
            ],
        )
        |
        Q(
            meeting_date__date__lt=today,
            developer__calling_status__in=[
                "Meeting",
                "Meeting_FollowUp",
            ],
        )
        |
        Q(
            meeting_date__date__lt=today,
            architect__calling_status__in=[
                "Meeting",
                "Meeting_FollowUp",
            ],
        )
        |
        Q(
            meeting_date__date__lt=today,
            engineer__calling_status__in=[
                "Meeting",
                "Meeting_FollowUp",
            ],
        )
    )


    # =========================================================
    # TYPE FILTER
    # =========================================================
    current_type = request.GET.get("type")

    if current_type not in [
        "Project",
        "Developer",
        "Architect",
        "Engineer",
    ]:
        current_type = None


    if current_type:
        meetings = meetings.filter(
            type=current_type
        )


    # =========================================================
    # QUICK FILTER
    # =========================================================
    current_filter = request.GET.get(
        "filter",
        "all"
    )


    if current_filter == "not_manage":

        meetings = meetings.filter(
            not_manage_q
        )

    elif current_filter == "today":

        meetings = meetings.filter(
            meeting_date__date=today
        )

    elif current_filter == "tomorrow":

        meetings = meetings.filter(
            meeting_date__date=tomorrow
        )

    elif current_filter == "upcoming":

        meetings = meetings.filter(
            meeting_date__date__gt=tomorrow
        )

    else:

        current_filter = "all"


    # =========================================================
    # DATE FILTER
    # =========================================================
    date_filter = request.GET.get(
        "date_filter",
        "all"
    )

    selected_date = request.GET.get(
        "selected_date",
        ""
    )

    date_from = request.GET.get(
        "date_from",
        ""
    )

    date_to = request.GET.get(
        "date_to",
        ""
    )


    # ---------------------------------------------------------
    # SPECIFIC DATE
    # ---------------------------------------------------------
    if (
        date_filter == "date"
        and selected_date
    ):

        try:

            selected_date_obj = datetime.strptime(
                selected_date,
                "%Y-%m-%d"
            ).date()


            meetings = meetings.filter(
                meeting_date__date=selected_date_obj
            )

        except ValueError:

            selected_date = ""
            date_filter = "all"


    # ---------------------------------------------------------
    # DATE RANGE
    # ---------------------------------------------------------
    elif (
        date_filter == "range"
        and date_from
        and date_to
    ):

        try:

            date_from_obj = datetime.strptime(
                date_from,
                "%Y-%m-%d"
            ).date()

            date_to_obj = datetime.strptime(
                date_to,
                "%Y-%m-%d"
            ).date()


            # Agar From date badi hai
            # To date se swap kar do
            if date_from_obj > date_to_obj:

                date_from_obj, date_to_obj = (
                    date_to_obj,
                    date_from_obj,
                )

                date_from, date_to = (
                    date_to,
                    date_from,
                )


            meetings = meetings.filter(
                meeting_date__date__range=(
                    date_from_obj,
                    date_to_obj,
                )
            )


        except ValueError:

            date_from = ""
            date_to = ""
            date_filter = "all"


    elif date_filter not in [
        "all",
        "date",
        "range",
    ]:

        date_filter = "all"


    # =========================================================
    # TOTAL TYPE COUNTS
    # =========================================================
    project_meeting_count = Meeting.objects.filter(
        type="Project"
    ).count()


    developer_meeting_count = Meeting.objects.filter(
        type="Developer"
    ).count()


    architect_meeting_count = Meeting.objects.filter(
        type="Architect"
    ).count()


    engineer_meeting_count = Meeting.objects.filter(
        type="Engineer"
    ).count()


    # =========================================================
    # QUICK FILTER COUNTS
    # =========================================================
    not_manage_count = Meeting.objects.filter(
        not_manage_q
    ).count()


    today_count = Meeting.objects.filter(
        meeting_date__date=today
    ).count()


    tomorrow_count = Meeting.objects.filter(
        meeting_date__date=tomorrow
    ).count()


    upcoming_count = Meeting.objects.filter(
        meeting_date__date__gt=tomorrow
    ).count()


    all_count = Meeting.objects.count()


    # =========================================================
    # TYPE + QUICK FILTER COUNTS
    # =========================================================
    def type_filter_count(
        meeting_type,
        filter_name
    ):

        qs = Meeting.objects.filter(
            type=meeting_type
        )


        if filter_name == "not_manage":

            qs = qs.filter(
                not_manage_q
            )

        elif filter_name == "today":

            qs = qs.filter(
                meeting_date__date=today
            )

        elif filter_name == "tomorrow":

            qs = qs.filter(
                meeting_date__date=tomorrow
            )

        elif filter_name == "upcoming":

            qs = qs.filter(
                meeting_date__date__gt=tomorrow
            )


        return qs.count()


    # =========================================================
    # CONTEXT
    # =========================================================
    context = {

        # -----------------------------------------------------
        # MEETINGS
        # -----------------------------------------------------
        "meetings": meetings,


        # -----------------------------------------------------
        # CURRENT FILTERS
        # -----------------------------------------------------
        "current_filter": current_filter,
        "current_type": current_type,


        # -----------------------------------------------------
        # DATE FILTER
        # -----------------------------------------------------
        "date_filter": date_filter,
        "selected_date": selected_date,
        "date_from": date_from,
        "date_to": date_to,


        # -----------------------------------------------------
        # TYPE COUNTS
        # -----------------------------------------------------
        "project_meeting_count":
            project_meeting_count,

        "developer_meeting_count":
            developer_meeting_count,

        "architect_meeting_count":
            architect_meeting_count,

        "engineer_meeting_count":
            engineer_meeting_count,


        # -----------------------------------------------------
        # QUICK FILTER COUNTS
        # -----------------------------------------------------
        "not_manage_count":
            not_manage_count,

        "today_count":
            today_count,

        "tomorrow_count":
            tomorrow_count,

        "upcoming_count":
            upcoming_count,

        "all_count":
            all_count,


        # -----------------------------------------------------
        # TYPE LABEL
        # -----------------------------------------------------
        "selected_type_label": (
            dict(
                Meeting.TYPE_CHOICES
            ).get(
                current_type
            )
            if current_type
            else ""
        ),


        # -----------------------------------------------------
        # FILTER LABEL
        # -----------------------------------------------------
        "selected_filter_label": {

            "not_manage": "Not Manage",

            "today": "Today",

            "tomorrow": "Tomorrow",

            "upcoming": "Upcoming",

            "all": "All Meetings",

        }.get(
            current_filter,
            "All Meetings",
        ),
    }


    # =========================================================
    # RENDER
    # =========================================================
    return render(
        request,
        "dashboard/meeting/property_meetings.html",
        context,
    )