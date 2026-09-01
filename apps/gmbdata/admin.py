from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (
    Realty,
    Interior,
    Refrense,
    Meeting,
    Followup,
    Comment,
    VoiceRecording,
    Visit,
)


from .resources_clean import (
    RealtyResource,
    RefrenseResource,
    InteriorResource
    
)

# =========================================================
# MEETING INLINE
# =========================================================

class MeetingInline(admin.StackedInline):
    model = Meeting
    extra = 0
    max_num = 1

    fields = (
        "meeting_no",
        "status",
        "meeting_date",
        "assigned_to",
        "comment",
    )

    readonly_fields = (
        "meeting_no",
    )


# =========================================================
# FOLLOWUP INLINE
# =========================================================

class FollowupInline(admin.StackedInline):
    model = Followup
    extra = 0
    max_num = 1

    fields = (
        "followup_no",
        "status",
        "followup_date",
        "assigned_to",
        "comment",
    )

    readonly_fields = (
        "followup_no",
    )


# =========================================================
# COMMENT INLINE
# =========================================================

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

    fields = (
        "comment",
    )


# =========================================================
# VOICE RECORDING INLINE
# =========================================================

class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 0


# =========================================================
# VISIT INLINE
# =========================================================

class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0

    fields = (
        "visit_date",
        "status",
        "assigned_to",
        "comment",
    )


# =========================================================
# REALTY ADMIN
# =========================================================

@admin.register(Realty)
class RealtyAdmin(ImportExportModelAdmin):

    resource_class = RealtyResource

    list_display = (
        "id",
        "name",
        "phone",
        "city_text",
        "state",
        "rating",
        "reviews",
        "status",
        "assigned_to",
        "is_verified",
        "is_featured",
        "is_active",
        "created_at",
    )

    search_fields = (
        "id",
        "name",
        "phone",
        "place_id",
        "google_id",
        "cid",
        "city_text",
        "state",
    )

    list_filter = (
        "status",
        "state",
        "country",
        "is_verified",
        "is_featured",
        "is_active",
        "assigned_to",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "slug",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "id",
                    "name",
                    "name_for_emails",
                    "category_text",
                    "type",
                    "phone",
                    "website",
                )
            },
        ),

        (
            "Location",
            {
                "fields": (
                    "city",
                    "locality",
                    "area",
                    "postal_code",
                    "address",
                    "street",
                    "city_text",
                    "state",
                    "postal_code_text",
                    "country",
                    "latitude",
                    "longitude",
                )
            },
        ),

        (
            "Google Information",
            {
                "fields": (
                    "place_id",
                    "google_id",
                    "cid",
                    "rating",
                    "reviews",
                    "business_status",
                    "working_hours",
                )
            },
        ),

        (
            "Content",
            {
                "fields": (
                    "description",
                    "about",
                    "logo",
                )
            },
        ),

        (
            "Status & Assignment",
            {
                "fields": (
                    "status",
                    "assigned_to",
                    "is_verified",
                    "is_featured",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "slug",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            # Agar BaseModel me created_by hai
            if hasattr(obj, "created_by"):
                obj.created_by = request.user

        # Agar BaseModel me updated_by hai
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)
# =========================================================
# REFRENSE ADMIN
# =========================================================



# =========================================================
# INTERIOR ADMIN
# =========================================================

@admin.register(Interior)
class InteriorAdmin(ImportExportModelAdmin):

    resource_class = InteriorResource

    # =====================================================
    # LIST DISPLAY
    # =====================================================

    list_display = (
        "id",
        "name",
        "phone",
        "other_phone",
        "city_text",
        "state",
        "rating",
        "reviews",
        "status",
        "assigned_to",
        "is_verified",
        "is_featured",
        "is_active",
    )

    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (
        "id",
        "name",
        "name_for_emails",
        "phone",
        "other_phone",
        "place_id",
        "google_id",
        "cid",
        "city_text",
        "state",
        "postal_code_text",
        "address",
    )

    # =====================================================
    # FILTER
    # =====================================================

    list_filter = (
        "status",
        "state",
        "country",
        "is_active",
        "is_verified",
        "is_featured",
        "assigned_to",
    )

    # =====================================================
    # ORDERING
    # =====================================================

    ordering = (
        "-created_at",
    )

    # =====================================================
    # DATE FILTER
    # =====================================================

    date_hierarchy = "created_at"

    # =====================================================
    # LIST PER PAGE
    # =====================================================

    list_per_page = 50

    # =====================================================
    # EDIT PAGE
    # =====================================================

    readonly_fields = (
        "id",
        "slug",
        "created_at",
        "updated_at",
    )

@admin.register(Refrense)
class RefrenseAdmin(ImportExportModelAdmin):

    resource_class = RefrenseResource
    

    # =====================================================
    # LIST DISPLAY
    # =====================================================

    list_display = (
        "id",
        "refrense_name",
        "contact_no",
        "other_no",
        "city",
        "locality",
        "area",
        "status",
        "assigned_to",
        "is_verified",
        "is_featured",
        "is_active",
        "created_at",
    )

    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (
        "id",
        "refrense_name",
        "contact_no",
        "other_no",
        "email",
        "address",
    )

    # =====================================================
    # FILTER
    # =====================================================

    list_filter = (
        "status",
        "is_verified",
        "is_featured",
        "is_active",
        "assigned_to",
        "city",
        "locality",
        "area",
    )

    # =====================================================
    # ORDERING
    # =====================================================

    ordering = (
        "-created_at",
    )

    # =====================================================
    # READONLY
    # =====================================================

    readonly_fields = (
        "id",
        "slug",
        "created_at",
        "updated_at",
    )

    # =====================================================
    # FIELDSETS
    # =====================================================

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "id",
                    "refrense_name",
                    "status",
                    "assigned_to",
                )
            },
        ),

        (
            "Location",
            {
                "fields": (
                    "city",
                    "locality",
                    "area",
                    "address",
                    "description",
                )
            },
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "contact_no",
                    "other_no",
                    "email",
                    "website",
                    "google_map",
                )
            },
        ),

        (
            "Google Information",
            {
                "fields": (
                    "rating",
                    "reviews_count",
                    "business_status_raw",
                )
            },
        ),

        (
            "Image",
            {
                "fields": (
                    "logo",
                    "logo_preview",
                )
            },
        ),

        (
            "Verification",
            {
                "fields": (
                    "is_verified",
                    "is_featured",
                    "is_active",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "slug",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # =====================================================
    # LOGO PREVIEW
    # =====================================================

    readonly_fields = (
        "id",
        "slug",
        "logo_preview",
        "created_at",
        "updated_at",
    )

    # =====================================================
    # AUTO USER
    # =====================================================

    def save_model(self, request, obj, form, change):

        if not change:

            if hasattr(obj, "created_by"):
                obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        super().save_model(
            request,
            obj,
            form,
            change,
        )
# =========================================================
# MEETING ADMIN
# =========================================================

@admin.register(Meeting)
class MeetingAdmin(ImportExportModelAdmin):


    list_display = (
        "id",
        "meeting_no",
        "realty",
        "status",
        "meeting_date",
        "assigned_to",
        "created_at",
    )

    search_fields = (
        "meeting_no",
        "realty__name",
        "realty__phone",
    )

    list_filter = (
        "status",
        "assigned_to",
    )

    readonly_fields = (
        "id",
        "meeting_no",
        "created_at",
        "updated_at",
    )


# =========================================================
# FOLLOWUP ADMIN
# =========================================================

@admin.register(Followup)
class FollowupAdmin(ImportExportModelAdmin):


    list_display = (
        "id",
        "followup_no",
        "realty",
        "status",
        "followup_date",
        "assigned_to",
        "created_at",
    )

    search_fields = (
        "followup_no",
        "realty__name",
        "realty__phone",
    )

    list_filter = (
        "status",
        "assigned_to",
    )

    readonly_fields = (
        "id",
        "followup_no",
        "created_at",
        "updated_at",
    )


# =========================================================
# COMMENT ADMIN
# =========================================================

@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):


    list_display = (
        "id",
        "realty",
        "comment",
        "created_by",
        "created_at",
    )

    search_fields = (
        "realty__name",
        "realty__phone",
        "comment",
    )

    readonly_fields = (
        "id",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )


# =========================================================
# VOICE RECORDING ADMIN
# =========================================================

@admin.register(VoiceRecording)
class VoiceRecordingAdmin(ImportExportModelAdmin):


    list_display = (
        "id",
        "realty",
        "file",
        "created_by",
        "created_at",
    )

    search_fields = (
        "realty__name",
        "realty__phone",
    )

    readonly_fields = (
        "id",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )


# =========================================================
# VISIT ADMIN
# =========================================================

@admin.register(Visit)
class VisitAdmin(ImportExportModelAdmin):


    list_display = (
        "id",
        "realty",
        "visit_date",
        "status",
        "assigned_to",
        "created_at",
    )

    search_fields = (
        "realty__name",
        "realty__phone",
    )

    list_filter = (
        "status",
        "assigned_to",
    )

    readonly_fields = (
        "id",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )