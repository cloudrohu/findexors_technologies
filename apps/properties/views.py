from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from .models import (
    Developer,
    Architects,
    Engineer,
    Project,
    Meeting,
)

from .forms import (
    DeveloperEditForm,
    ArchitectEditForm,
    EngineerEditForm,
    ProjectEditForm,
    MeetingEditForm,
)


# ============================================================
# PROPERTY MEETINGS
# ============================================================

@login_required
def property_meetings(request):

    today = timezone.localdate()
    tomorrow = today + timezone.timedelta(days=1)

    # --------------------------------------------------------
    # BASE QUERY
    # --------------------------------------------------------

    meetings = (
        Meeting.objects
        .select_related(
            "developer",
            "architect",
            "engineer",
            "project",
            "assigned_to",
        )
        .order_by("-meeting_date", "-created_at")
    )

    # --------------------------------------------------------
    # NOT MANAGE
    #
    # Past meeting + parent still has:
    # Meeting / Meeting_FollowUp
    # --------------------------------------------------------

    not_manage_q = (
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
        |
        Q(
            meeting_date__date__lt=today,
            project__calling_status__in=[
                "Meeting",
                "Meeting_FollowUp",
            ],
        )
    )

    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    current_filter = request.GET.get(
        "filter",
        "all",
    )

    current_type = request.GET.get(
        "type",
        "all",
    )

    # --------------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------------

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

    # all = no date filter

    # --------------------------------------------------------
    # TYPE FILTER
    # --------------------------------------------------------

    if current_type in [
        "Developer",
        "Architect",
        "Engineer",
        "Project",
    ]:

        meetings = meetings.filter(
            type=current_type
        )

    # ========================================================
    # COUNTS
    # ========================================================

    all_count = Meeting.objects.count()

    today_count = Meeting.objects.filter(
        meeting_date__date=today
    ).count()

    tomorrow_count = Meeting.objects.filter(
        meeting_date__date=tomorrow
    ).count()

    upcoming_count = Meeting.objects.filter(
        meeting_date__date__gt=tomorrow
    ).count()

    not_manage_count = Meeting.objects.filter(
        not_manage_q
    ).count()

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

    # ========================================================
    # CONTEXT
    # ========================================================

    context = {

        "meetings": meetings,

        # Date filters
        "current_filter": current_filter,

        "all_count": all_count,
        "today_count": today_count,
        "tomorrow_count": tomorrow_count,
        "upcoming_count": upcoming_count,
        "not_manage_count": not_manage_count,

        # Type filters
        "current_type": current_type,

        "project_meeting_count": project_meeting_count,
        "developer_meeting_count": developer_meeting_count,
        "architect_meeting_count": architect_meeting_count,
        "engineer_meeting_count": engineer_meeting_count,

        # Dates
        "today": today,
        "tomorrow": tomorrow,
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
def edit_developer(
    request,
    developer_id,
):

    developer = get_object_or_404(
        Developer,
        pk=developer_id,
    )

    # --------------------------------------------------------
    # GET MEETING ID
    #
    # Example:
    # ?meeting_id=MT000001
    # --------------------------------------------------------

    meeting_id = request.GET.get(
        "meeting_id"
    )

    if request.method == "POST":

        form = DeveloperEditForm(
            request.POST,
            request.FILES,
            instance=developer,
        )

        if form.is_valid():

            form.save()

            # ----------------------------------------------
            # Return to meeting if came from meeting card
            # ----------------------------------------------

            if meeting_id:

                return redirect(
                    "edit_meeting",
                    meeting_id=meeting_id,
                )

            return redirect(
                "property_meetings"
            )

    else:

        form = DeveloperEditForm(
            instance=developer,
        )

    return render(
        request,
        "dashboard/meeting/edit_developer.html",
        {
            "form": form,
            "developer": developer,
            "meeting_id": meeting_id,
        },
    )


# ============================================================
# EDIT ARCHITECT
# ============================================================

@login_required
def edit_architect(
    request,
    architect_id,
):

    architect = get_object_or_404(
        Architects,
        pk=architect_id,
    )

    meeting_id = request.GET.get(
        "meeting_id"
    )

    if request.method == "POST":

        form = ArchitectEditForm(
            request.POST,
            request.FILES,
            instance=architect,
        )

        if form.is_valid():

            form.save()

            if meeting_id:

                return redirect(
                    "edit_meeting",
                    meeting_id=meeting_id,
                )

            return redirect(
                "property_meetings"
            )

    else:

        form = ArchitectEditForm(
            instance=architect,
        )

    return render(
        request,
        "dashboard/meeting/edit_architect.html",
        {
            "form": form,
            "architect": architect,
            "meeting_id": meeting_id,
        },
    )


# ============================================================
# EDIT ENGINEER
# ============================================================

@login_required
def edit_engineer(
    request,
    engineer_id,
):

    engineer = get_object_or_404(
        Engineer,
        pk=engineer_id,
    )

    meeting_id = request.GET.get(
        "meeting_id"
    )

    if request.method == "POST":

        form = EngineerEditForm(
            request.POST,
            request.FILES,
            instance=engineer,
        )

        if form.is_valid():

            form.save()

            if meeting_id:

                return redirect(
                    "edit_meeting",
                    meeting_id=meeting_id,
                )

            return redirect(
                "property_meetings"
            )

    else:

        form = EngineerEditForm(
            instance=engineer,
        )

    return render(
        request,
        "dashboard/meeting/edit_engineer.html",
        {
            "form": form,
            "engineer": engineer,
            "meeting_id": meeting_id,
        },
    )


# ============================================================
# EDIT PROJECT
# ============================================================

@login_required
def edit_project(
    request,
    project_id,
):

    project = get_object_or_404(
        Project,
        pk=project_id,
    )

    meeting_id = request.GET.get(
        "meeting_id"
    )

    if request.method == "POST":

        form = ProjectEditForm(
            request.POST,
            request.FILES,
            instance=project,
        )

        if form.is_valid():

            form.save()

            if meeting_id:

                return redirect(
                    "edit_meeting",
                    meeting_id=meeting_id,
                )

            return redirect(
                "property_meetings"
            )

    else:

        form = ProjectEditForm(
            instance=project,
        )

    return render(
        request,
        "dashboard/meeting/edit_project.html",
        {
            "form": form,
            "project": project,
            "meeting_id": meeting_id,
        },
    )


# ============================================================
# EDIT MEETING
# ============================================================

@login_required
def edit_meeting(
    request,
    meeting_id,
):

    meeting = get_object_or_404(
        Meeting.objects.select_related(
            "developer",
            "architect",
            "engineer",
            "project",
            "assigned_to",
        ),
        pk=meeting_id,
    )

    # --------------------------------------------------------
    # FIND PARENT
    # --------------------------------------------------------

    parent = None
    parent_type = None

    if meeting.developer:

        parent = meeting.developer
        parent_type = "Developer"

    elif meeting.architect:

        parent = meeting.architect
        parent_type = "Architect"

    elif meeting.engineer:

        parent = meeting.engineer
        parent_type = "Engineer"

    elif meeting.project:

        parent = meeting.project
        parent_type = "Project"

    # --------------------------------------------------------
    # FORM
    # --------------------------------------------------------

    if request.method == "POST":

        form = MeetingEditForm(
            request.POST,
            instance=meeting,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "property_meetings"
            )

    else:

        form = MeetingEditForm(
            instance=meeting,
        )

    # --------------------------------------------------------
    # PARENT EDIT URL INFORMATION
    # --------------------------------------------------------

    parent_edit_url = None

    if meeting.developer:

        parent_edit_url = (
            "edit_developer"
        )

    elif meeting.architect:

        parent_edit_url = (
            "edit_architect"
        )

    elif meeting.engineer:

        parent_edit_url = (
            "edit_engineer"
        )

    elif meeting.project:

        parent_edit_url = (
            "edit_project"
        )

    return render(
        request,
        "dashboard/meeting/edit_meeting.html",
        {
            "form": form,
            "meeting": meeting,
            "parent": parent,
            "parent_type": parent_type,
            "parent_edit_url": parent_edit_url,
        },
    )





# ============================================================
# PROPERTY DEVELOPERS
# ============================================================

@login_required
def property_developers(request):

    developers = Developer.objects.all().order_by("-id")

    return render(
        request,
        "dashboard/property/developers.html",
        {
            "developers": developers,
        }
    )


# ============================================================
# PROPERTY ARCHITECTS
# ============================================================

@login_required
def property_architects(request):

    architects = Architects.objects.all().order_by("-id")

    return render(
        request,
        "dashboard/property/architects.html",
        {
            "architects": architects,
        }
    )


# ============================================================
# PROPERTY ENGINEERS
# ============================================================

@login_required
def property_engineers(request):

    engineers = Engineer.objects.all().order_by("-id")

    return render(
        request,
        "dashboard/property/engineers.html",
        {
            "engineers": engineers,
        }
    )


@login_required
def property_projects(request):

    search = request.GET.get("search", "").strip()
    developer_id = request.GET.get("developer", "").strip()
    property_type = request.GET.get("property_type", "").strip()
    city = request.GET.get("city", "").strip()
    locality = request.GET.get("locality", "").strip()
    bhk = request.GET.get("bhk", "").strip()
    construction_status = request.GET.get("construction_status", "").strip()
    featured = request.GET.get("featured", "").strip()
    active = request.GET.get("active", "").strip()
    calling = request.GET.get("calling", "").strip()


    # =====================================================
    # PROJECT QUERYSET
    # =====================================================

    projects = (
        Project.objects
        .select_related(
            "developer",
            "architect",
            "engineer",
            "city",
            "locality",
            "area",
            "postal_code",
            "property_type",
            "possession_year",
        )
        .prefetch_related(
            "contact_persons",
            "headers",
            "welcomes",
            "sliders",
            "overviews",
            "aboutus",
            "usps",
            "configurations",
            "configs",
            "amenities",
            "gallery",
            "rera",
            "why_invest",
            "bank_offers",
            "faqs",
            "enquiries",
            "comments",
            "voice_recordings",
            "visits",
        )
        .order_by("-id")
    )


    # =====================================================
    # SEARCH
    # =====================================================

    if search:
        projects = projects.filter(
            project_name__icontains=search
        )


    # =====================================================
    # DEVELOPER
    # =====================================================

    if developer_id:
        projects = projects.filter(
            developer_id=developer_id
        )


    # =====================================================
    # PROPERTY TYPE
    # =====================================================

    if property_type:
        projects = projects.filter(
            property_type_id=property_type
        )


    # =====================================================
    # CITY
    # =====================================================

    if city:
        projects = projects.filter(
            city_id=city
        )


    # =====================================================
    # LOCALITY
    # =====================================================

    if locality:
        projects = projects.filter(
            locality_id=locality
        )


    # =====================================================
    # BHK
    # =====================================================

    if bhk:
        projects = projects.filter(
            bhk_type=bhk
        )


    # =====================================================
    # CONSTRUCTION STATUS
    # =====================================================

    if construction_status:
        projects = projects.filter(
            construction_status=construction_status
        )


    # =====================================================
    # FEATURED
    # =====================================================

    if featured == "yes":

        projects = projects.filter(
            featured_property=True
        )

    elif featured == "no":

        projects = projects.filter(
            featured_property=False
        )


    # =====================================================
    # ACTIVE / INACTIVE
    # =====================================================

    if active == "yes":

        projects = projects.filter(
            is_active=True
        )

    elif active == "no":

        projects = projects.filter(
            is_active=False
        )


    # =====================================================
    # CALLING
    # =====================================================

    if calling:
        projects = projects.filter(
            calling_status=calling
        )

    # =====================================================
    # PAGINATION
    # =====================================================

    paginator = Paginator(
        projects,
        12
    )

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)


    # Compact pagination
    page_range = paginator.get_elided_page_range(
        number=page_obj.number,
        on_each_side=2,
        on_ends=1,
    )


    # =====================================================
    # PAGINATION QUERY STRING
    # =====================================================

    pagination_params = request.GET.copy()

    if "page" in pagination_params:
        pagination_params.pop("page")

    pagination_query = pagination_params.urlencode()

        # =====================================================
        # FILTER OPTIONS
        # =====================================================

    developers = (
        Developer.objects
        .all()
        .order_by("title")
    )


    property_types = (
        Project.objects
        .exclude(property_type__isnull=True)
        .values(
            "property_type_id",
            "property_type__name",
        )
        .distinct()
        .order_by("property_type__name")
    )


    cities = (
        Project.objects
        .exclude(city__isnull=True)
        .values(
            "city_id",
            "city__name",
        )
        .distinct()
        .order_by("city__name")
    )


    localities = (
        Project.objects
        .exclude(locality__isnull=True)
        .values(
            "locality_id",
            "locality__name",
        )
        .distinct()
        .order_by("locality__name")
    )


    bhk_choices = (
        Project.objects
        .exclude(bhk_type__isnull=True)
        .exclude(bhk_type="")
        .values_list(
            "bhk_type",
            flat=True
        )
        .distinct()
        .order_by("bhk_type")
    )


    construction_choices = (
        Project.objects
        .exclude(
            construction_status__isnull=True
        )
        .exclude(
            construction_status=""
        )
        .values_list(
            "construction_status",
            flat=True
        )
        .distinct()
        .order_by("construction_status")
    )


    calling_choices = (
        Project.objects
        .exclude(
            calling_status__isnull=True
        )
        .exclude(
            calling_status=""
        )
        .values_list(
            "calling_status",
            flat=True
        )
        .distinct()
        .order_by("calling_status")
    )


    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        # PAGINATED PROJECTS
        "projects": page_obj,


        "page_obj": page_obj,
        "paginator": paginator,
        "page_range": page_range,
        "pagination_query": pagination_query,


        # FILTER VALUES
        "search": search,
        "developer_id": developer_id,
        "property_type": property_type,
        "city": city,
        "locality": locality,
        "bhk": bhk,
        "construction_status": construction_status,
        "featured": featured,
        "active": active,
        "calling": calling,


        # FILTER OPTIONS
        "developers": developers,
        "property_types": property_types,
        "cities": cities,
        "localities": localities,
        "bhk_choices": bhk_choices,
        "construction_choices": construction_choices,
        "calling_choices": calling_choices,
    }


    return render(
        request,
        "dashboard/property/projects.html",
        context,
    )
@login_required
def property_project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    return render(
        request,
        "dashboard/property/project_detail.html",
        {
            "project": project,
        }
    )