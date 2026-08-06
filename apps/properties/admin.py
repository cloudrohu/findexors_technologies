from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin


from .models import *

from .models import (
    Developer,
    Architects,
    Engineer,
    Project,

    BookingOffer,
    WelcomeTo,
    WebSlider,
    Overview,
    AboutUs,
    USP,
    Configuration,
    Connectivity,
    Amenities,
    Gallery,
    Header,
    RERA_Info,
    WhyInvest,
    BankOffer,
    ProjectFAQ,
    Enquiry,
    ProjectContactPerson,

    Comment,
    VoiceRecording,
    Visit,
    Followup,
    Meeting,
)

NO_IMAGE = "https://via.placeholder.com/70x70?text=No+Image"




class BaseAdmin(admin.ModelAdmin):

    save_on_top = True

    list_per_page = 30

    actions = (
        "make_active",
        "make_inactive",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.action(description="✅ Mark selected as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="❌ Mark selected as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):

        if hasattr(obj, "created_by"):

            if not obj.pk:
                obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        super().save_model(
            request,
            obj,
            form,
            change,
        )



class ImagePreviewMixin:

    image_field = "image"

    def image_preview(self, obj):

        image = getattr(obj, self.image_field, None)

        if image and hasattr(image, "url"):
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                image.url,
            )

        return "-"

    image_preview.short_description = "Preview"


class LogoPreviewMixin:

    logo_field = "logo"

    def logo_preview(self, obj):

        logo = getattr(obj, self.logo_field, None)

        if logo and hasattr(logo, "url"):

            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                logo.url,
            )

        return "-"

    logo_preview.short_description = "Logo"


# =====================================================
# BASE ADMIN
# =====================================================

class BaseCRMAdmin(ImportExportModelAdmin):

    save_on_top = True

    list_per_page = 50

    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    search_fields = (
        "title",
        "contact_person",
        "contact_no",
        "email",
    )

    list_filter = (
        "is_active",
        "is_verified",
        "is_featured",
        "calling_status",
    )

    list_editable = (
        "is_active",
        "is_verified",
        "is_featured",
    )

    ordering = (
        "-created_at",
    )

    def logo_preview(self, obj):

        if getattr(obj, "logo", None):

            return format_html(
                '<img src="{}" style="height:55px;border-radius:6px;">',
                obj.logo.url,
            )

        return "-"

    logo_preview.short_description = "Logo"


# =====================================================
# INLINE
# =====================================================

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 0


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0


class FollowupInline(admin.StackedInline):
    model = Followup
    extra = 0
    max_num = 1


class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 0
    max_num = 1


# =====================================================
# PROJECT INLINES
# =====================================================

class BookingOfferInline(admin.TabularInline):
    model = BookingOffer
    extra = 1


class WelcomeToInline(admin.StackedInline):
    model = WelcomeTo
    extra = 1


class WebSliderInline(admin.TabularInline):
    model = WebSlider
    extra = 1


class OverviewInline(admin.TabularInline):
    model = Overview
    extra = 1


class AboutUsInline(admin.StackedInline):
    model = AboutUs
    extra = 1


class USPInline(admin.TabularInline):
    model = USP
    extra = 1


class ConfigurationInline(admin.TabularInline):
    model = Configuration
    extra = 1


class ConnectivityInline(admin.TabularInline):
    model = Connectivity
    extra = 1


class AmenitiesInline(admin.TabularInline):
    model = Amenities
    extra = 1


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


class HeaderInline(admin.StackedInline):
    model = Header
    extra = 0
    max_num = 1


class RERAInline(admin.StackedInline):
    model = RERA_Info
    extra = 0
    max_num = 1


class WhyInvestInline(admin.TabularInline):
    model = WhyInvest
    extra = 1


class BankOfferInline(admin.TabularInline):
    model = BankOffer
    extra = 1


class FAQInline(admin.TabularInline):
    model = ProjectFAQ
    extra = 1


class ContactPersonInline(admin.TabularInline):
    model = ProjectContactPerson
    extra = 1


class EnquiryInline(admin.TabularInline):
    model = Enquiry
    extra = 0
    can_delete = False
    readonly_fields = (
        "name",
        "phone",
        "email",
        "message",
        "contacted_on",
    )

# =====================================================
# DEVELOPER ADMIN
# =====================================================
@admin.register(Developer)
class DeveloperAdmin(
    BaseAdmin,
    LogoPreviewMixin,
    ImportExportModelAdmin,
):

    list_display = (
        "title",
        "city",
        "locality",
        "contact_person",
        "contact_no",
        "calling_status",
        "featured_builder",
        "is_active",
        "logo_preview",
        
    )

    list_display_links = (
        "title",
    )

    list_editable = (
        "featured_builder",
        "is_active",
    )

    search_fields = (
        "title",
        "contact_person",
        "contact_no",
        "email",
        "city__name",
        "locality__name",
        "postal_code__code",
    )

    autocomplete_fields = (
        "city",
        "locality",
        "area",
        "postal_code",
        "assigned_to",
    )

    list_filter = (
        "calling_status",
        "featured_builder",
        "is_active",
        "city",
    )

    readonly_fields = (
        "slug",
        "logo_preview",
        "created_at",
        "updated_at",
    )

    

    fieldsets = (

        ("Basic Information", {
            "fields": (
                "title",
                "slug",
                "logo",
                "logo_preview",
            )
        }),

        ("Location", {
            "fields": (
                "city",
                "locality",
                "area",
                "postal_code",
                "address",
                "google_map",
            )
        }),

        ("Contact", {
            "fields": (
                "contact_person",
                "contact_no",
                "email",
                "web_site",
            )
        }),

        ("Description", {
            "fields": (
                "keywords",
                "about_developer",
                "note",
            )
        }),

        ("Status", {
            "fields": (
                "calling_status",
                "assigned_to",
                "featured_builder",
                "is_featured",
                "is_verified",
                "is_active",
            )
        }),

        ("System", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    save_on_top = True
    list_per_page = 30


# =====================================================
# ARCHITECT ADMIN
# =====================================================
@admin.register(Architects)
class ArchitectAdmin(
    BaseAdmin,
    LogoPreviewMixin,
    ImportExportModelAdmin,
):
    list_display = (
        "title",
        "city",
        "contact_person",
        "contact_no",
        "calling_status",
        "featured_architect",
        "is_active",
        "logo_preview",
    )

    list_display_links = ("title",)

    list_editable = (
        "featured_architect",
        "is_active",
    )

    search_fields = (
        "title",
        "contact_person",
        "contact_no",
        "email",
    )

    autocomplete_fields = (
        "city",
        "locality",
        "area",
        "postal_code",
        "assigned_to",
    )

    list_filter = (
        "calling_status",
        "featured_architect",
        "is_active",
        "city",
    )

    readonly_fields = (
        "slug",
        "logo_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        ("Basic Information", {
            "fields": (
                "title",
                "slug",
                "logo",
                "logo_preview",
            )
        }),

        ("Location", {
            "fields": (
                "city",
                "locality",
                "area",
                "postal_code",
                "address",
                "google_map",
            )
        }),

        ("Contact", {
            "fields": (
                "contact_person",
                "contact_no",
                "email",
                "web_site",
            )
        }),

        ("Description", {
            "fields": (
                "keywords",
                "about_architect",
                "note",
            )
        }),

        ("Status", {
            "fields": (
                "calling_status",
                "assigned_to",
                "featured_architect",
                "is_featured",
                "is_verified",
                "is_active",
            )
        }),

        ("System", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    save_on_top = True
    list_per_page = 30


# =====================================================
# ENGINEER ADMIN
# =====================================================
@admin.register(Engineer)
class EngineerAdmin(
    BaseAdmin,
    LogoPreviewMixin,
    ImportExportModelAdmin,
):
    list_display = (
        "title",
        "city",
        "contact_person",
        "contact_no",
        "calling_status",
        "featured_engineer",
        "is_active",
        "logo_preview",
    )

    list_display_links = ("title",)

    list_editable = (
        "featured_engineer",
        "is_active",
    )

    search_fields = (
        "title",
        "contact_person",
        "contact_no",
        "email",
    )

    autocomplete_fields = (
        "city",
        "locality",
        "area",
        "postal_code",
        "assigned_to",
    )

    list_filter = (
        "calling_status",
        "featured_engineer",
        "is_active",
        "city",
    )

    readonly_fields = (
        "slug",
        "logo_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        ("Basic Information", {
            "fields": (
                "title",
                "slug",
                "logo",
                "logo_preview",
            )
        }),

        ("Location", {
            "fields": (
                "city",
                "locality",
                "area",
                "postal_code",
                "address",
                "google_map",
            )
        }),

        ("Contact", {
            "fields": (
                "contact_person",
                "contact_no",
                "email",
                "web_site",
            )
        }),

        ("Description", {
            "fields": (
                "keywords",
                "about_engineer",
                "note",
            )
        }),

        ("Status", {
            "fields": (
                "calling_status",
                "assigned_to",
                "featured_engineer",
                "is_featured",
                "is_verified",
                "is_active",
            )
        }),

        ("System", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    save_on_top = True
    list_per_page = 30


# =====================================================
# PROJECT ADMIN
# =====================================================

@admin.register(Project)
class ProjectAdmin(
    BaseAdmin,
    ImagePreviewMixin,
    ImportExportModelAdmin,
    DraggableMPTTAdmin,
):
    image_field = "image"
    mptt_indent_field = "project_name"

    list_display = (
        "tree_actions",
        "indented_title",
        "developer",
        "city",
        "locality",
        "construction_status",
        "featured_property",
        "is_active",
        "image_preview",
    )

    list_display_links = (
        "indented_title",
    )

    list_editable = (
        "featured_property",
        "is_active",
    )

    search_fields = (
        "project_name",
        "developer__title",
        "city__name",
        "locality__name",
        "slug",
    )

    autocomplete_fields = (
        "parent",
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

    list_filter = (
        "construction_status",
        "featured_property",
        "is_active",
        "developer",
        "city",
        "property_type",
    )

    readonly_fields = (
        "slug",
        "image_preview",
        "created_at",
        "updated_at",
    )

    

    ordering = (
        "tree_id",
        "lft",
    )

    save_on_top = True

    list_per_page = 30

    inlines = [
        BookingOfferInline,
        WelcomeToInline,
        WebSliderInline,
        OverviewInline,
        AboutUsInline,
        USPInline,
        ConfigurationInline,
        ConnectivityInline,
        AmenitiesInline,
        GalleryInline,
        HeaderInline,
        RERAInline,
        WhyInvestInline,
        BankOfferInline,
        FAQInline,
        ContactPersonInline,
        EnquiryInline,
    ]

    fieldsets = (

        ("Basic Information", {
            "fields": (
                "parent",
                "project_name",
                "slug",
                "image",
                "image_preview",
            )
        }),

        ("Project Information", {
            "fields": (
                "developer",
                "architect",
                "engineer",
                "property_type",
                "construction_status",
                "calling_status",
            )
        }),

        ("Location", {
            "fields": (
                "city",
                "locality",
                "area",
                "postal_code",
                "address",
                "google_map_iframe",
            )
        }),

        ("Configuration", {
            "fields": (
                "bhk_type",
                "floor",
                "land_parcel",
                "luxurious",
                "pricing",
                "balcony",
            )
        }),

        ("Possession", {
            "fields": (
                "possession_year",
                "possession_month",
                "occupancy_certificate",
                "commencement_certificate",
            )
        }),

        ("Media", {
            "fields": (
                "youtube_embed_id",
            )
        }),

        ("Status", {
            "fields": (
                "featured_property",
                "is_active",
            )
        }),

        
    )


    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Image"




# =====================================================
# VOICE RECORDING
# =====================================================

@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):

    list_display = (
        "type",
        "developer",
        "architect",
        "engineer",
        "project",
        "uploaded_by",
        "created_at",
    )

    autocomplete_fields = (
        "developer",
        "architect",
        "engineer",
        "project",
        "uploaded_by",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
    )

    list_filter = (
        "type",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30


# =====================================================
# VISIT
# =====================================================

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):

    list_display = (
        "type",
        "visit_for",
        "visit_type",
        "visit_status",
        "developer",
        "architect",
        "engineer",
        "project",
        "created_at",
    )

    autocomplete_fields = (
        "developer",
        "architect",
        "engineer",
        "project",
        "created_by",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
        "comment",
    )

    list_filter = (
        "type",
        "visit_for",
        "visit_status",
        "visit_type",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30


# =====================================================
# FOLLOWUP
# =====================================================

@admin.register(Followup)
class FollowupAdmin(admin.ModelAdmin):

    list_display = (
        "type",
        "status",
        "followup_date",
        "assigned_to",
        "developer",
        "architect",
        "engineer",
        "project",
    )

    autocomplete_fields = (
        "developer",
        "architect",
        "engineer",
        "project",
        "assigned_to",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
        "comment",
    )

    list_filter = (
        "type",
        "status",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-followup_date",
    )

    list_per_page = 30


# =====================================================
# MEETING
# =====================================================

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):

    list_display = (
        "type",
        "status",
        "meeting_date",
        "assigned_to",
        "developer",
        "architect",
        "engineer",
        "project",
    )

    autocomplete_fields = (
        "developer",
        "architect",
        "engineer",
        "project",
        "assigned_to",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
        "comment",
    )

    list_filter = (
        "type",
        "status",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-meeting_date",
    )

    list_per_page = 30


# =====================================================
# BASE ADMIN
# =====================================================
