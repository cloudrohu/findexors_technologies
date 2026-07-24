from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from .base import MasterBaseModel



class Location(MPTTModel, MasterBaseModel):
    LOCATION_TYPES = (
        ("COUNTRY", "Country"),
        ("STATE", "State"),
        ("DISTRICT", "District"),
        ("CITY", "City"),
        ("LOCALITY", "Locality"),
        ("SUBLOCALITY", "Sub Locality"),
        ("AREA", "Area"),
        ("PINCODE", "Pincode"),
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Parent Location",
    )

    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPES,
        db_index=True,
    )

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Required only for PINCODE type",
    )

    is_top_city = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ["tree_id", "lft"]

    def __str__(self):
        return " / ".join(
            node.name for node in self.get_ancestors(include_self=True)
        )

    @property
    def full_name(self):
        return self.__str__()




class Postal_Code(models.Model):
    postal_name = models.CharField(max_length=500, blank=True, null=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.postal_name} - {self.postal_code}"
    
    class Meta:
        verbose_name_plural='Postal_Code' 
