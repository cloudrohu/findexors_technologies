from django import forms
from django.contrib import admin
from django.utils.html import format_html
from ..filters import (
    StateFilter,
    DistrictCityFilter,
    LocalityFilter,
)
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
            LocationType.DISTRICT_CITY: [LocationType.STATE],
            LocationType.LOCALITY_AREA: [LocationType.DISTRICT_CITY],
            LocationType.SUBLOCALITY_AREA: [LocationType.LOCALITY_AREA],
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



class LocationAdminForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        parent_map = {
            LocationType.STATE: [LocationType.COUNTRY],
            LocationType.DISTRICT_CITY: [LocationType.STATE],
            LocationType.LOCALITY_AREA: [LocationType.DISTRICT_CITY],
            LocationType.SUBLOCALITY_AREA: [LocationType.LOCALITY_AREA],
        }

        # ----------------------------
        # Get selected location type
        # ----------------------------

        location_type = None

        # POST request (after validation error)
        if self.data.get("location_type"):
            location_type = self.data.get("location_type")

        # Edit page
        elif self.instance.pk:
            location_type = self.instance.location_type

        # ----------------------------
        # Parent queryset
        # ----------------------------

        if location_type in parent_map:

            self.fields["parent"].queryset = Location.objects.filter(
                location_type__in=parent_map[location_type],
                is_active=True,
            ).order_by("name")

        elif location_type == LocationType.COUNTRY:

            self.fields["parent"].queryset = Location.objects.none()

        else:
            # Add page
            self.fields["parent"].queryset = Location.objects.filter(
                is_active=True
            ).order_by("tree_id", "lft")


    autocomplete_fields = (
        "parent",
    )

    search_fields = (
        "name",
        "code",
        "slug",
        "parent__name",
    )


    list_display = (
        "tree_actions",
        "indented_title",
        "parent",
        "location_badge",
        "is_top_city",
        "is_active",
    )


    list_filter = (
        "location_type",
        StateFilter,
        DistrictCityFilter,
        LocalityFilter,
        "is_top_city",
        "is_active",
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