from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    CompanyIndustry,
    CompanyType,
    CompanySize,
    Company,
    Branch,
    Department,
    Designation,
    CompanyContact,
    CompanyDocument,
)


class MasterAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "is_active",
    )

    search_fields = (
        "name",
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

    ordering = (
        "name",
    )

    save_on_top = True


@admin.register(CompanyIndustry)
class CompanyIndustryAdmin(MasterAdmin):
    pass


@admin.register(CompanyType)
class CompanyTypeAdmin(MasterAdmin):
    pass