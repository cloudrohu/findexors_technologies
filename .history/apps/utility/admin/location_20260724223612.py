from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from import_export.admin import ImportExportModelAdmin
from apps.utility.models import Location,PostalCode


@admin.register(Location)
class LocationAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"

    list_display = (
        "tree_actions",
        "indented_title",
        "location_type",
        "postal_code",
        "is_top_city",
        "is_active",
    )

    list_display_links = ("indented_title",)

    search_fields = (
        "name",
        "postal_code",
    )

    list_filter = (
        "location_type",
        "is_active",
        "is_top_city",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }



@admin.register(PostalCode)
class Postal_CodeAdmin(ImportExportModelAdmin):

    list_display = ("postal_name","postal_code")
    ordering = ("postal_name","postal_code")
    search_fields = ("postal_name","postal_code")
    list_per_page = 30