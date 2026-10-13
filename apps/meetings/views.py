from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from apps.properties.models import Meeting


@login_required
def property_meetings(request):

    today = timezone.localdate()
    tomorrow = today + timezone.timedelta(days=1)

    # =========================================================
    # BASE QUERY
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

    valid_types = [
        "Project",
        "Developer",
        "Architect",
        "Engineer",
    ]

    if current_type not in valid_types:
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
        "all",
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
        "all",
    )

    selected_date = request.GET.get(
        "selected_date",
        "",
    )

    date_from = request.GET.get(
        "date_from",
        "",
    )

    date_to = request.GET.get(
        "date_to",
        "",
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
                "%Y-%m-%d",
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
                "%Y-%m-%d",
            ).date()

            date_to_obj = datetime.strptime(
                date_to,
                "%Y-%m-%d",
            ).date()

            # Automatically swap if From > To
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
    # GLOBAL COUNTS
    # =========================================================

    all_count = Meeting.objects.count()

    project_all_count = Meeting.objects.filter(
        type="Project"
    ).count()

    developer_all_count = Meeting.objects.filter(
        type="Developer"
    ).count()

    architect_all_count = Meeting.objects.filter(
        type="Architect"
    ).count()

    engineer_all_count = Meeting.objects.filter(
        type="Engineer"
    ).count()

    # =========================================================
    # GLOBAL QUICK FILTER COUNTS
    # =========================================================

    not_manage_count = (
        Meeting.objects
        .filter(not_manage_q)
        .count()
    )

    today_count = Meeting.objects.filter(
        meeting_date__date=today
    ).count()

    tomorrow_count = Meeting.objects.filter(
        meeting_date__date=tomorrow
    ).count()

    upcoming_count = Meeting.objects.filter(
        meeting_date__date__gt=tomorrow
    ).count()

    # =========================================================
    # TYPE + QUICK FILTER COUNT
    # =========================================================

    def type_filter_count(
        meeting_type,
        filter_name,
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
    # TYPE COUNTS
    # =========================================================

    project_not_manage_count = type_filter_count(
        "Project",
        "not_manage",
    )

    project_today_count = type_filter_count(
        "Project",
        "today",
    )

    project_tomorrow_count = type_filter_count(
        "Project",
        "tomorrow",
    )

    project_upcoming_count = type_filter_count(
        "Project",
        "upcoming",
    )

    developer_not_manage_count = type_filter_count(
        "Developer",
        "not_manage",
    )

    developer_today_count = type_filter_count(
        "Developer",
        "today",
    )

    developer_tomorrow_count = type_filter_count(
        "Developer",
        "tomorrow",
    )

    developer_upcoming_count = type_filter_count(
        "Developer",
        "upcoming",
    )

    architect_not_manage_count = type_filter_count(
        "Architect",
        "not_manage",
    )

    architect_today_count = type_filter_count(
        "Architect",
        "today",
    )

    architect_tomorrow_count = type_filter_count(
        "Architect",
        "tomorrow",
    )

    architect_upcoming_count = type_filter_count(
        "Architect",
        "upcoming",
    )

    engineer_not_manage_count = type_filter_count(
        "Engineer",
        "not_manage",
    )

    engineer_today_count = type_filter_count(
        "Engineer",
        "today",
    )

    engineer_tomorrow_count = type_filter_count(
        "Engineer",
        "tomorrow",
    )

    engineer_upcoming_count = type_filter_count(
        "Engineer",
        "upcoming",
    )

    # =========================================================
    # LABELS
    # =========================================================

    type_labels = dict(
        Meeting.TYPE_CHOICES
    )

    selected_type_label = (
        type_labels.get(current_type)
        if current_type
        else ""
    )

    selected_filter_label = {
        "not_manage": "Not Manage",
        "today": "Today",
        "tomorrow": "Tomorrow",
        "upcoming": "Upcoming",
        "all": "All Meetings",
    }.get(
        current_filter,
        "All Meetings",
    )

    # =========================================================
    # CONTEXT
    # =========================================================

    context = {

        "meetings": meetings,

        # Current filters
        "current_filter": current_filter,
        "current_type": current_type,

        # Date filter
        "date_filter": date_filter,
        "selected_date": selected_date,
        "date_from": date_from,
        "date_to": date_to,

        # Labels
        "selected_type_label": selected_type_label,
        "selected_filter_label": selected_filter_label,

        # Global counts
        "all_count": all_count,
        "not_manage_count": not_manage_count,
        "today_count": today_count,
        "tomorrow_count": tomorrow_count,
        "upcoming_count": upcoming_count,

        # Project
        "project_all_count": project_all_count,
        "project_not_manage_count": project_not_manage_count,
        "project_today_count": project_today_count,
        "project_tomorrow_count": project_tomorrow_count,
        "project_upcoming_count": project_upcoming_count,

        # Developer
        "developer_all_count": developer_all_count,
        "developer_not_manage_count": developer_not_manage_count,
        "developer_today_count": developer_today_count,
        "developer_tomorrow_count": developer_tomorrow_count,
        "developer_upcoming_count": developer_upcoming_count,

        # Architect
        "architect_all_count": architect_all_count,
        "architect_not_manage_count": architect_not_manage_count,
        "architect_today_count": architect_today_count,
        "architect_tomorrow_count": architect_tomorrow_count,
        "architect_upcoming_count": architect_upcoming_count,

        # Engineer
        "engineer_all_count": engineer_all_count,
        "engineer_not_manage_count": engineer_not_manage_count,
        "engineer_today_count": engineer_today_count,
        "engineer_tomorrow_count": engineer_tomorrow_count,
        "engineer_upcoming_count": engineer_upcoming_count,
    }

    return render(
        request,
        "dashboard/meeting/property_meetings.html",
        context,
    )