from django.contrib import admin
from .models import (
    Response,
    Meeting,
    Followup,
    Comment,
    VoiceRecording,
)

# =====================================================
# 🔹 AUTO USER MIXIN
# =====================================================

class AutoUserAdminMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not change and not getattr(obj, "created_by", None):
            obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        if hasattr(obj, "created_by") and not getattr(obj, "created_by", None):
            obj.created_by = request.user

        super().save_model(request, obj, form, change)



    def save_formset(self, request, form, formset, change):

        instances = formset.save(commit=False)

        # ----------------------------
        # Delete selected inline objects
        # ----------------------------
        for obj in formset.deleted_objects:

            response = getattr(obj, "response", None)

            obj.delete()

            # Refresh Response Status
            if response:
                response.refresh_status()

        # ----------------------------
        # Save new/updated inline objects
        # ----------------------------
        for obj in instances:

            if hasattr(obj, "created_by") and not getattr(obj, "created_by", None):
                obj.created_by = request.user

            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user

            obj.save()

            # Refresh Response Status
            if hasattr(obj, "response"):
                obj.response.refresh_status()

        formset.save_m2m()


# =====================================================
# 🔹 MAGIC SEARCH MIXIN
# =====================================================

class MagicSearchMixin:
    prefix_map = {}

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if not search_term:
            return queryset, use_distinct

        term = search_term.upper().strip()

        for prefix, field in self.prefix_map.items():
            if term.startswith(prefix):
                queryset |= self.model.objects.filter(**{field: term})





        if term.isdigit():
            if hasattr(self.model, "response"):
                queryset |= self.model.objects.filter(response__contact_no__icontains=term)
            elif hasattr(self.model, "contact_no"):
                queryset |= self.model.objects.filter(contact_no__icontains=term)

        return queryset, use_distinct


# =====================================================
# 🔹 INLINE CLASSES
# =====================================================

class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True

    readonly_fields = (
        "meeting_no",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 1
    max_num = 1
    can_delete = True
    show_change_link = True

    readonly_fields = (
        "followup_no",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    show_change_link = True

    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    show_change_link = True

    readonly_fields = (
        "created_at",
        "created_by",
    )


from django.utils.html import format_html
from django.contrib import admin

# =====================================================
# 🔹 RESPONSE ADMIN (PRO VERSION)
# =====================================================

@admin.register(Response)
class ResponseAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {
        "R": "response_no",
    }

    STATUS_COLORS = {
        "New": "#2563eb",
        "Meeting": "#0ea5e9",
        "Follow_Up": "#f59e0b",
        "Meeting_FollowUp": "#8b5cf6",
        "Deal_close": "#16a34a",
        "Fake_lead": "#dc2626",
        "Training": "#7c3aed",
        "For_job": "#6366f1",
        "Software_company": "#0891b2",
        "Not_received": "#6b7280",
    }

    inlines = [
        MeetingInline,
        FollowupInline,
        CommentInline,
        VoiceRecordingInline,
    ]

    list_display = (
        "response_id",
        "colored_status",
        "lead_source",
        "contact_no",
        "contact_persone",
        "business_name",
        "city",
        "assigned_to",
        "converted_badge",
        "created_at",
    )

    list_display_links = (
        "response_id",
        "contact_persone",
        "business_name",
    )

    search_fields = (
        "response_no",
        "contact_no",
        "contact_persone",
        "business_name",
    )

    list_filter = (
        "status",
        "lead_source",
        "assigned_to",
        "business_category",
        "city",
        "locality",
        "is_converted",
        "created_at",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_select_related = (
        "assigned_to",
        "business_category",
        "city",
        "locality",
        "area",
        "postal_code",
    )

    filter_horizontal = (
        "requirement_types",
    )

    readonly_fields = (
        "response_no",
        "converted_at",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    fieldsets = (

        (
            "Response Information",
            {
                "fields": (
                    "response_no",
                    "status",
                    "lead_source",
                    "assigned_to",
                    "is_converted",
                    "converted_at",
                )
            },
        ),

        (
            "Business Details",
            {
                "fields": (
                    "business_name",
                    "business_category",
                    "contact_persone",
                    "contact_no",
                    "requirement_types",
                )
            },
        ),

        (
            "Location Details",
            {
                "fields": (
                    "city",
                    "locality",
                    "area",
                    "postal_code",
                    "address",
                )
            },
        ),

        (
            "WhatsApp Tracking",
            {
                "fields": (
                    "whatsapp_welcome_sent",
                    "whatsapp_followup_1_sent",
                    "whatsapp_followup_2_sent",
                ),
                "classes": ("collapse",),
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_by",
                    "updated_by",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # ==========================================
    # Display Methods
    # ==========================================

    @admin.display(description="Response ID", ordering="response_no")
    def response_id(self, obj):
        return format_html(
            '<span style="font-weight:700;color:#2563eb;">{}</span>',
            obj.response_no,
        )

    @admin.display(description="Conversion")
    def converted_badge(self, obj):

        color = "#16a34a" if obj.is_converted else "#dc2626"
        text = "Converted" if obj.is_converted else "Pending"

        return format_html(
            '<span style="background:{};color:#fff;padding:4px 10px;border-radius:20px;font-weight:600;">{}</span>',
            color,
            text,
        )

    @admin.display(description="Status", ordering="status")
    def colored_status(self, obj):

        color = self.STATUS_COLORS.get(obj.status, "#6b7280")

        return format_html(
            "<strong style='color:{}'>{}</strong>",
            color,
            obj.get_status_display(),
        )


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {
        "RM": "meeting_no",
        "R": "response__response_no",
    }

    list_display = (
        "meeting_id",
        "response_id",
        "response_business",
        "status_badge",
        "meeting_date",
        "assigned_to",
        "created_at",
    )

    list_display_links = (
        "meeting_id",
        "response_business",
    )

    search_fields = (
        "meeting_no",
        "response__response_no",
        "response__contact_no",
        "response__contact_persone",
        "response__business_name",
    )

    list_filter = (
        "status",
        "assigned_to",
        "meeting_date",
        "response__status",
        "response__lead_source",
        "response__city",
        "response__locality",
        "created_at",
    )

    ordering = ("-meeting_date",)

    date_hierarchy = "meeting_date"

    list_select_related = (
        "response",
        "assigned_to",
    )

    readonly_fields = (
        "meeting_no",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    fieldsets = (

        (
            "Meeting Information",
            {
                "fields": (
                    "meeting_no",
                    "response",
                    "status",
                    "meeting_date",
                    "assigned_to",
                    "comment",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_by",
                    "updated_by",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # ==========================================
    # DISPLAY METHODS
    # ==========================================

    @admin.display(
        description="Meeting ID",
        ordering="meeting_no",
    )
    def meeting_id(self, obj):
        return format_html(
            '<span style="font-weight:700;color:#2563eb;">{}</span>',
            obj.meeting_no,
        )

    @admin.display(
        description="Response ID",
        ordering="response__response_no",
    )
    def response_id(self, obj):
        return obj.response.response_no

    @admin.display(
        description="Business",
        ordering="response__business_name",
    )
    def response_business(self, obj):
        return obj.response.business_name or "-"

    @admin.display(
        description="Status",
        ordering="status",
    )
    def status_badge(self, obj):

        colors = {
            "New Meeting": "#2563eb",
            "Re Meeting": "#f59e0b",
            "Cancelled": "#dc2626",
            "Deal Done": "#16a34a",
        }

        color = colors.get(obj.status, "#6b7280")

        return format_html(
            '<span style="background:{};color:white;padding:4px 10px;border-radius:20px;font-weight:600;">{}</span>',
            color,
            obj.status,
        )
# =====================================================
# 🔹 FOLLOWUP ADMIN
# =====================================================


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {
        "RF": "followup_no",
        "R": "response__response_no",
    }

    list_display = (
        "followup_id",
        "response_id",
        "response_business",
        "status_badge",
        "followup_date",
        "assigned_to",
        "created_at",
    )

    list_display_links = (
        "followup_id",
        "response_business",
    )

    search_fields = (
        "followup_no",
        "response__response_no",
        "response__contact_no",
        "response__contact_persone",
        "response__business_name",
    )

    list_filter = (
        "status",
        "assigned_to",
        "followup_date",
        "response__status",
        "response__lead_source",
        "response__city",
        "response__locality",
        "created_at",
    )

    ordering = ("-followup_date",)

    date_hierarchy = "followup_date"

    list_select_related = (
        "response",
        "assigned_to",
    )

    readonly_fields = (
        "followup_no",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    fieldsets = (

        (
            "Follow Up Information",
            {
                "fields": (
                    "followup_no",
                    "response",
                    "status",
                    "followup_date",
                    "assigned_to",
                    "comment",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_by",
                    "updated_by",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # ==========================================
    # DISPLAY METHODS
    # ==========================================

    @admin.display(
        description="Followup ID",
        ordering="followup_no",
    )
    def followup_id(self, obj):
        return format_html(
            '<span style="font-weight:700;color:#2563eb;">{}</span>',
            obj.followup_no,
        )

    @admin.display(
        description="Response ID",
        ordering="response__response_no",
    )
    def response_id(self, obj):
        return obj.response.response_no

    @admin.display(
        description="Business",
        ordering="response__business_name",
    )
    def response_business(self, obj):
        return obj.response.business_name or "-"

    @admin.display(
        description="Status",
        ordering="status",
    )
    def status_badge(self, obj):

        colors = {
            "New Followup": "#2563eb",
            "Re Followup": "#f59e0b",
            "Cancelled": "#dc2626",
            "Deal Done": "#16a34a",
        }

        color = colors.get(obj.status, "#6b7280")

        return format_html(
            '<span style="background:{};color:white;padding:4px 10px;border-radius:20px;font-weight:600;">{}</span>',
            color,
            obj.status,
        )
# =====================================================
# 🔹 COMMENT ADMIN
# =====================================================
@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {"CM": "id", "MR": "response__id"}

    list_display = (
        "cm_id",
        "response",
        "comment",
        "created_by",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
        "comment",
    )

    list_filter = (
        "response__status",
        "response__lead_source",
        "response__city",
        "response__locality",
        "created_at",
    )

    ordering = ("-created_at",)

    list_select_related = ("response",)

    def cm_id(self, obj):
        return f"CM{str(obj.id).zfill(3)}"

    cm_id.short_description = "Comment ID"
# =====================================================
# 🔹 VOICE RECORDING ADMIN
# =====================================================

@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    prefix_map = {"VR": "id", "MR": "response__id"}

    list_display = (
        "vr_id",
        "response",
        "note",
        "created_by",
        "created_at",
    )

    search_fields = (
        "response__contact_no",
        "response__business_name",
        "note",
    )

    list_filter = (
        "response__status",
        "response__lead_source",
        "response__city",
        "response__locality",
        "created_at",
    )

    ordering = ("-created_at",)

    list_select_related = ("response",)

    def vr_id(self, obj):
        return f"VR{str(obj.id).zfill(3)}"

    vr_id.short_description = "Recording ID"# =====================================================
# 🔹 STAFF ADMIN
# =====================================================
