from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin

from apps.utility.models import (
    LeadSource,
    LeadStatus,
    LeadPriority,
    InquiryType,
    RequirementType,
    ContactType,
    Occupation,
    CompanyType,
)


class MasterAdmin(ImportExportModelAdmin):
    """
    Generic admin for all master tables.
    """

    list_display = (
        "name",
        "code",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "slug",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "name",
    )

    save_on_top = True

    list_per_page = 50


@admin.register(LeadSource)
class LeadSourceAdmin(MasterAdmin):
    pass


@admin.register(LeadPriority)
class LeadPriorityAdmin(MasterAdmin):
    pass


@admin.register(InquiryType)
class InquiryTypeAdmin(MasterAdmin):
    pass


@admin.register(RequirementType)
class RequirementTypeAdmin(MasterAdmin):
    pass


@admin.register(ContactType)
class ContactTypeAdmin(MasterAdmin):
    pass


@admin.register(Occupation)
class OccupationAdmin(MasterAdmin):
    pass


@admin.register(CompanyType)
class CompanyTypeAdmin(MasterAdmin):
    pass


@admin.register(LeadStatus)
class LeadStatusAdmin(MasterAdmin):

    list_display = (
        "name",
        "code",
        "color_preview",
        "is_active",
    )

    fields = (
        "name",
        "code",
        "slug",
        "color",
        "description",
        "sort_order",
        "is_active",
    )

    @admin.display(description="Color")
    def color_preview(self, obj):
        return format_html(
            '<span style="display:inline-block;width:22px;height:22px;border-radius:50%;background:{};"></span> {}',
            obj.color,
            obj.color,
        )