from django.contrib import admin

from apps.utility.models import (
    PropertyType,
    UnitType,
    Furnishing,
    Facing,
    ConstructionStatus,
    OwnershipType,
    ParkingType,
    Amenity,
)

from .base import MasterAdmin


@admin.register(PropertyType)
class PropertyTypeAdmin(MasterAdmin):
    pass


@admin.register(UnitType)
class UnitTypeAdmin(MasterAdmin):
    pass


@admin.register(Furnishing)
class FurnishingAdmin(MasterAdmin):
    pass


@admin.register(Facing)
class FacingAdmin(MasterAdmin):
    pass


@admin.register(ConstructionStatus)
class ConstructionStatusAdmin(MasterAdmin):
    pass


@admin.register(OwnershipType)
class OwnershipTypeAdmin(MasterAdmin):
    pass


@admin.register(ParkingType)
class ParkingTypeAdmin(MasterAdmin):
    pass


@admin.register(Amenity)
class AmenityAdmin(MasterAdmin):
    list_display = (
        "name",
        "code",
        "icon",
        "is_active",
    )