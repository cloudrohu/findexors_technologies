from django.db import models

from .base import MasterBaseModel

class PropertyType(MasterBaseModel):
    class Meta:
        verbose_name = "Property Type"
        verbose_name_plural = "Property Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class UnitType(MasterBaseModel):
    class Meta:
        verbose_name = "Unit Type"
        verbose_name_plural = "Unit Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Furnishing(MasterBaseModel):
    class Meta:
        verbose_name = "Furnishing"
        verbose_name_plural = "Furnishings"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Facing(MasterBaseModel):
    class Meta:
        verbose_name = "Facing"
        verbose_name_plural = "Facings"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ConstructionStatus(MasterBaseModel):
    class Meta:
        verbose_name = "Construction Status"
        verbose_name_plural = "Construction Statuses"
        ordering = ["name"]

    def __str__(self):
        return self.name


class OwnershipType(MasterBaseModel):
    class Meta:
        verbose_name = "Ownership Type"
        verbose_name_plural = "Ownership Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ParkingType(MasterBaseModel):
    class Meta:
        verbose_name = "Parking Type"
        verbose_name_plural = "Parking Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Amenity(MasterBaseModel):
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome class (e.g. fa-solid fa-dumbbell)",
    )

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"
        ordering = ["name"]

    def __str__(self):
        return self.name