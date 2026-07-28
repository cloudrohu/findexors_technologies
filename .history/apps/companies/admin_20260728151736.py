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


@admin.register(CompanySize)
class CompanySizeAdmin(MasterAdmin):
    pass

class BranchInline(admin.TabularInline):
    model = Branch
    extra = 0


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0


class CompanyContactInline(admin.TabularInline):
    model = CompanyContact
    extra = 0


class CompanyDocumentInline(admin.TabularInline):
    model = CompanyDocument
    extra = 0



@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):

    list_display = (
        "name",
        "industry",
        "company_type",
        "company_size",
        "phone",
        "email",
        "location",
        "is_verified",
        "is_active",
    )

    list_filter = (
        "industry",
        "company_type",
        "company_size",
        "is_verified",
        "is_active",
    )

    search_fields = (
        "name",
        "legal_name",
        "email",
        "phone",
        "gst_number",
        "pan_number",
    )

    autocomplete_fields = (
        "industry",
        "company_type",
        "company_size",
        "location",
        "postal_code",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_editable = (
        "is_verified",
        "is_active",
    )

    inlines = [
        BranchInline,
        DepartmentInline,
        CompanyContactInline,
        CompanyDocumentInline,
    ]

    save_on_top = True



@admin.register(Branch)
class BranchAdmin(ImportExportModelAdmin):

    list_display = (
        "name",
        "company",
        "manager_name",
        "phone",
        "location",
        "is_active",
    )

    list_filter = (
        "company",
        "is_active",
    )

    search_fields = (
        "name",
        "company__name",
        "manager_name",
    )

    autocomplete_fields = (
        "company",
        "location",
        "postal_code",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    save_on_top = True



@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):

    list_display = (
        "name",
        "company",
        "is_active",
    )

    list_filter = (
        "company",
        "is_active",
    )

    search_fields = (
        "name",
        "company__name",
    )

    autocomplete_fields = (
        "company",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    save_on_top = True



@admin.register(Designation)
class DesignationAdmin(ImportExportModelAdmin):

    list_display = (
        "name",
        "department",
        "is_active",
    )

    list_filter = (
        "department",
        "is_active",
    )

    search_fields = (
        "name",
        "department__name",
    )

    autocomplete_fields = (
        "department",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    save_on_top = True
