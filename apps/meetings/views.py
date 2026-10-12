from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from apps.properties.models import Meeting


def property_meetings(request):

    today = timezone.localdate()
    tomorrow = today + timezone.timedelta(days=1)

    meetings = Meeting.objects.all()

    # -----------------------------------------
    # NOT MANAGE
    # Past meeting + parent still pending
    # -----------------------------------------
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

    # -----------------------------------------
    # FILTER
    # -----------------------------------------
    current_filter = request.GET.get("filter", "all")

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

    elif current_filter == "all":

        meetings = meetings

    # -----------------------------------------
    # COUNTS
    # -----------------------------------------
    project_count = Meeting.objects.filter(
        type="Project"
    ).count()

    developer_count = Meeting.objects.filter(
        type="Developer"
    ).count()

    architect_count = Meeting.objects.filter(
        type="Architect"
    ).count()

    engineer_count = Meeting.objects.filter(
        type="Engineer"
    ).count()

    # -----------------------------------------
    # FILTER COUNTS
    # -----------------------------------------
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

    context = {
        # Meeting type cards
        "project_meeting_count": project_count,
        "developer_meeting_count": developer_count,
        "architect_meeting_count": architect_count,
        "engineer_meeting_count": engineer_count,

        # Filter counts
        "not_manage_count": not_manage_count,
        "today_count": today_count,
        "tomorrow_count": tomorrow_count,
        "upcoming_count": upcoming_count,
        "all_count": all_count,

        # Meeting list
        "meetings": meetings,
        "current_filter": current_filter,
    }

    return render(
        request,
        "dashboard/meeting/property_meetings.html",
        context
    )