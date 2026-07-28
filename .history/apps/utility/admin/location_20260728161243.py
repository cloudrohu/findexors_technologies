from django import forms
from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from apps.utility.models import (
    Location,
    PostalCode,
    LocationType,
)


# ==========================================================
# Location Admin Form
# ==========================================================

class LocationAdminForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["parent"].queryset = Location.objects.all()

        location_type = (
            self.instance.location_type
            if self.instance.pk
            else self.initial.get("location_type")
        )

        parent_map = {
            LocationType.STATE: [LocationType.COUNTRY],
            LocationType.DISTRICT: [LocationType.STATE],
            LocationType.LOCALITY: [LocationType.DISTRICT],
            LocationType.SUBLOCALITY: [LocationType.LOCALITY],
        }

        allowed_parent_types = parent_map.get(location_type)

        if allowed_parent_types:
            self.fields["parent"].queryset = Location.objects.filter(
                location_type__in=allowed_parent_types
            )
        else:
            self.fields["parent"].queryset = Location.objects.none()


# ==========================================================
# Location Admin
# ==========================================================

@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):

    form = LocationAdminForm

    mptt_indent_field = "name"

    list_display = (
        "tree_actions",
        "indented_title",
        "location_badge",
        "is_top_city",
        "is_active",
    )

    list_display_links = (
        "indented_title",
    )

    search_fields = (
        "name",
        "code",
        "slug",
    )

    list_filter = (
        "location_type",
        "is_top_city",
        "is_active",
    )

    list_editable = (
        "is_top_city",
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
        "tree_id",
        "lft",
    )

    save_on_top = True

    list_per_page = 50

    @admin.display(description="Type")
    def location_badge(self, obj):

        colors = {
            LocationType.COUNTRY: "#0d6efd",
            LocationType.STATE: "#198754",
            LocationType.DISTRICT: "#fd7e14",
            LocationType.LOCALITY: "#20c997",
            LocationType.SUBLOCALITY: "#dc3545",
        }

        color = colors.get(obj.location_type, "#6c757d")

        return format_html(
            """
            <span style="
                background:{};
                color:white;
                padding:4px 10px;
                border-radius:16px;
                font-size:12px;
                font-weight:600;
            ">
                {}
            </span>
            """,
            color,
            obj.get_location_type_display(),
        )


# ==========================================================
# Postal Code Admin
# ==========================================================

@admin.register(PostalCode)
class PostalCodeAdmin(ImportExportModelAdmin):

    list_display = (
        "code",
        "location",
        "is_active",
    )

    search_fields = (
        "code",
        "location__name",
    )

    list_filter = (
        "location__location_type",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "location",
    )

    ordering = (
        "code",
    )

    save_on_top = True

    list_per_page = 50