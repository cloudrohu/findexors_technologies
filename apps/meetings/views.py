
from apps.properties.models import Developer, Meeting

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.db.models import Q
from django.utils import timezone
# ============================================================
# PROPERTY MEETING
# ============================================================

@login_required
def property_meetings(request):

    today = timezone.localdate()
    tomorrow = today + timezone.timedelta(days=1)

    meetings = Meeting.objects.select_related(
        "developer",
        "architect",
        "engineer",
        "project",
        "assigned_to",
    ).all()

    # --------------------------------------------------------
    # NOT MANAGE
    # Past meeting + parent still pending
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # TYPE
    # --------------------------------------------------------

    current_type = request.GET.get("type")

    if current_type in [
        "Project",
        "Developer",
        "Architect",
        "Engineer",
    ]:
        meetings = meetings.filter(type=current_type)

    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    current_filter = request.GET.get("filter", "all")

    if current_filter == "not_manage":
        meetings = meetings.filter(not_manage_q)

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
        pass

    # --------------------------------------------------------
    # TYPE COUNTS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # GLOBAL FILTER COUNTS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # TYPE + FILTER COUNTS
    # --------------------------------------------------------

    def type_filter_count(meeting_type, filter_name):

        qs = Meeting.objects.filter(
            type=meeting_type
        )

        if filter_name == "not_manage":
            qs = qs.filter(not_manage_q)

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

    context = {

        # ------------------------------------
        # TYPE COUNTS
        # ------------------------------------

        "project_meeting_count":
            project_meeting_count,

        "developer_meeting_count":
            developer_meeting_count,

        "architect_meeting_count":
            architect_meeting_count,

        "engineer_meeting_count":
            engineer_meeting_count,

        # ------------------------------------
        # GLOBAL FILTER COUNTS
        # ------------------------------------

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

        # ------------------------------------
        # TYPE FILTER COUNTS
        # ------------------------------------

        "project_not_manage_count":
            type_filter_count("Project", "not_manage"),

        "project_today_count":
            type_filter_count("Project", "today"),

        "project_tomorrow_count":
            type_filter_count("Project", "tomorrow"),

        "project_upcoming_count":
            type_filter_count("Project", "upcoming"),

        "project_all_count":
            type_filter_count("Project", "all"),

        "developer_not_manage_count":
            type_filter_count("Developer", "not_manage"),

        "developer_today_count":
            type_filter_count("Developer", "today"),

        "developer_tomorrow_count":
            type_filter_count("Developer", "tomorrow"),

        "developer_upcoming_count":
            type_filter_count("Developer", "upcoming"),

        "developer_all_count":
            type_filter_count("Developer", "all"),

        "architect_not_manage_count":
            type_filter_count("Architect", "not_manage"),

        "architect_today_count":
            type_filter_count("Architect", "today"),

        "architect_tomorrow_count":
            type_filter_count("Architect", "tomorrow"),

        "architect_upcoming_count":
            type_filter_count("Architect", "upcoming"),

        "architect_all_count":
            type_filter_count("Architect", "all"),

        "engineer_not_manage_count":
            type_filter_count("Engineer", "not_manage"),

        "engineer_today_count":
            type_filter_count("Engineer", "today"),

        "engineer_tomorrow_count":
            type_filter_count("Engineer", "tomorrow"),

        "engineer_upcoming_count":
            type_filter_count("Engineer", "upcoming"),

        "engineer_all_count":
            type_filter_count("Engineer", "all"),

        # ------------------------------------
        # RESULT
        # ------------------------------------

        "meetings": meetings,

        "current_filter":
            current_filter,

        "current_type":
            current_type,

        "selected_type_label": (
            dict(Meeting.TYPE_CHOICES).get(
                current_type
            )
            if current_type
            else ""
        ),

        "selected_filter_label": {
            "not_manage": "Not Manage",
            "today": "Today",
            "tomorrow": "Tomorrow",
            "upcoming": "Upcoming",
            "all": "All Meetings",
        }.get(
            current_filter,
            "All Meetings"
        ),
    }

    return render(
        request,
        "dashboard/meeting/property_meetings.html",
        context,
    )


# ============================================================
# EDIT DEVELOPER
# ============================================================

@login_required
def edit_meeting_developer(request, pk):

    meeting = get_object_or_404(
        Meeting.objects.select_related("developer"),
        pk=pk,
    )

    if not meeting.developer:
        messages.error(
            request,
            "This meeting is not connected to a developer."
        )

        return redirect(
            "property_meetings"
        )

    developer = meeting.developer

    if request.method == "POST":

        # Basic
        developer.title = request.POST.get(
            "title",
            ""
        ).strip()

        developer.contact_person = request.POST.get(
            "contact_person",
            ""
        ).strip()

        developer.contact_no = request.POST.get(
            "contact_no",
            ""
        ).strip()

        developer.email = request.POST.get(
            "email",
            ""
        ).strip()

        developer.google_map = request.POST.get(
            "google_map",
            ""
        ).strip()

        developer.web_site = request.POST.get(
            "web_site",
            ""
        ).strip()

        # Location
        developer.address = request.POST.get(
            "address",
            ""
        ).strip()

        developer.keywords = request.POST.get(
            "keywords",
            ""
        ).strip()

        developer.about_developer = request.POST.get(
            "about_developer",
            ""
        ).strip()

        developer.note = request.POST.get(
            "note",
            ""
        ).strip()

        # Status
        developer.calling_status = request.POST.get(
            "calling_status",
            developer.calling_status,
        )

        developer.featured_builder = (
            request.POST.get("featured_builder")
            == "on"
        )

        developer.is_verified = (
            request.POST.get("is_verified")
            == "on"
        )

        developer.is_featured = (
            request.POST.get("is_featured")
            == "on"
        )

        developer.is_active = (
            request.POST.get("is_active")
            == "on"
        )

        # Logo
        if request.FILES.get("logo"):
            developer.logo = request.FILES["logo"]

        developer.updated_by = request.user

        developer.save()

        messages.success(
            request,
            "Developer updated successfully."
        )

        return redirect(
            request.POST.get(
                "next",
                f"/dashboard/meeting/property/?type=Developer&filter=all"
            )
        )

    context = {
        "developer": developer,
        "meeting": meeting,
    }

    return render(
        request,
        "dashboard/meeting/edit_developer.html",
        context,
    )


# ============================================================
# EDIT MEETING
# ============================================================

@login_required
def edit_property_meeting(request, pk):

    meeting = get_object_or_404(
        Meeting.objects.select_related(
            "developer",
            "architect",
            "engineer",
            "project",
            "assigned_to",
        ),
        pk=pk,
    )

    if request.method == "POST":

        meeting.status = request.POST.get(
            "status",
            meeting.status,
        )

        meeting.meeting_date = request.POST.get(
            "meeting_date"
        ) or None

        meeting.comment = request.POST.get(
            "comment",
            ""
        ).strip()

        assigned_to_id = request.POST.get(
            "assigned_to"
        )

        if assigned_to_id:
            from django.contrib.auth import get_user_model

            User = get_user_model()

            meeting.assigned_to = get_object_or_404(
                User,
                pk=assigned_to_id,
            )
        else:
            meeting.assigned_to = None

        meeting.updated_by = request.user

        meeting.save()

        messages.success(
            request,
            "Meeting updated successfully."
        )

        return redirect(
            request.POST.get(
                "next",
                "/dashboard/meeting/property/?filter=all"
            )
        )

    from django.contrib.auth import get_user_model

    User = get_user_model()

    users = User.objects.filter(
        is_active=True
    ).order_by(
        "first_name",
        "last_name",
        "username",
    )

    context = {
        "meeting": meeting,
        "users": users,
    }

    return render(
        request,
        "dashboard/meeting/edit_meeting.html",
        context,
    )