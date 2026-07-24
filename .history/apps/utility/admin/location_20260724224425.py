from django import forms
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from apps.utility.models import Location, PostalCode, LocationType


class LocationAdminForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get("instance")

        if instance:
            parent_map = {
                LocationType.STATE: LocationType.COUNTRY,
                LocationType.DISTRICT: LocationType.STATE,
                LocationType.CITY: LocationType.DISTRICT,
                LocationType.LOCALITY: LocationType.CITY,
                LocationType.SUBLOCALITY: LocationType.LOCALITY,
                LocationType.AREA: LocationType.SUBLOCALITY,
            }

            parent_type = parent_map.get(instance.location_type)

            if parent_type:
                self.fields["parent"].queryset = Location.objects.filter(
                    location_type=parent_type
                )

@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):
    form = LocationAdminForm
    mptt_indent_field = "name"

    list_display = (
        "tree_actions",
        "indented_title",
        "location_type",
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
        "is_active",
        "is_top_city",
    )

    list_editable = (
        "is_top_city",
        "is_active",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "tree_id",
        "lft",
    )


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
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    ordering = (
        "code",
    )


