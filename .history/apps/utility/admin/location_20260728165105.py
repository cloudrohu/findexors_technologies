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