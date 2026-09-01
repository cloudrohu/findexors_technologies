import re

from import_export import resources

from .models import Realty,Refrense

from apps.utility.models import (
    Location,
    LocationType,
    PostalCode,
)


# =========================================================
# PHONE CLEANER
# =========================================================

def clean_phone_last10(phone):
    """
    Phone number se:
    +91
    spaces
    -
    ()
    etc. remove karke
    sirf last 10 digits rakhta hai.
    """

    if not phone:
        return None

    phone = str(phone).strip()

    # Sirf digits rakho
    digits = re.sub(r"\D", "", phone)

    if len(digits) >= 10:
        return digits[-10:]

    return digits or None


# =========================================================
# GENERIC LOCATION NAME FINDER
# =========================================================

def get_location_name_field():
    """
    Location model mein actual name field automatically find karega.
    """

    possible_fields = [
        "name",
        "title",
        "location_name",
        "city_name",
        "locality_name",
    ]

    model_fields = {
        field.name
        for field in Location._meta.fields
    }

    for field_name in possible_fields:
        if field_name in model_fields:
            return field_name

    return None


# =========================================================
# REALTY RESOURCE
# =========================================================

class RealtyResource(resources.ModelResource):

    class Meta:

        model = Realty

        # Existing record ko place_id ke basis par update karega
        import_id_fields = ("place_id",)

        skip_unchanged = True
        report_skipped = True

        # =================================================
        # IMPORTANT
        # =================================================
        # BaseModel ke fields yahan intentionally nahi hain:
        #
        # id
        # created_at
        # updated_at
        # created_by
        # updated_by
        #
        # Ye CSV se import nahi honge.
        # =================================================

        fields = (

            # ---------------------------------------------
            # BASIC
            # ---------------------------------------------

            "name",
            "name_for_emails",

            # ---------------------------------------------
            # LOCATION TEXT / DISPLAY DATA
            # ---------------------------------------------

            "city",
            "locality",
            "area",
            "postal_code",

            "address",

            # ---------------------------------------------
            # GOOGLE DATA
            # ---------------------------------------------

            "category_text",
            "type",
            "phone",
            "website",
            "street",
            "city_text",
            "state",
            "postal_code_text",
            "country",

            "latitude",
            "longitude",

            "rating",
            "reviews",

            "place_id",
            "google_id",
            "cid",

            "business_status",
            "working_hours",

            "description",
            "about",
            "logo",

            # ---------------------------------------------
            # STATUS
            # ---------------------------------------------

            "status",

            # ---------------------------------------------
            # FLAGS
            # ---------------------------------------------

            "is_verified",
            "is_featured",
        )


    # =====================================================
    # LOCATION FINDER
    # =====================================================

    def get_location(
        self,
        name,
        location_type,
        parent=None,
    ):
        """
        Location ko name + location_type + parent ke basis par find karega.

        Example:

        Ahmedabad
            ↓
        Satellite
            ↓
        Makarba
        """

        if not name:
            return None

        name = str(name).strip()

        if not name or name in ("-", "--", "None", "null"):
            return None

        name_field = get_location_name_field()

        if not name_field:
            return None

        filters = {
            name_field: name,
            "location_type": location_type,
        }

        # ---------------------------------------------
        # Parent Mapping
        # ---------------------------------------------

        if parent is not None:

            # Location model mein parent_id expected hai
            filters["parent_id"] = parent.pk

        # ---------------------------------------------
        # Exact match
        # ---------------------------------------------

        location = Location.objects.filter(
            **filters
        ).first()

        if location:
            return location

        # ---------------------------------------------
        # Case insensitive fallback
        # ---------------------------------------------

        icase_filters = {
            f"{name_field}__iexact": name,
            "location_type": location_type,
        }

        if parent is not None:
            icase_filters["parent_id"] = parent.pk

        return Location.objects.filter(
            **icase_filters
        ).first()


    # =====================================================
    # POSTAL CODE FINDER
    # =====================================================

    def get_postal_code(self, value):
        """
        PostalCode model ke actual field ko automatically detect
        karke object find karega.
        """

        if not value:
            return None

        value = str(value).strip()

        if not value or value in ("-", "--", "None", "null"):
            return None

        possible_fields = [
            "postal_code",
            "code",
            "pincode",
            "pin_code",
            "name",
        ]

        model_fields = {
            field.name
            for field in PostalCode._meta.fields
        }

        field_name = None

        for possible in possible_fields:
            if possible in model_fields:
                field_name = possible
                break

        if not field_name:
            return None

        # Exact
        obj = PostalCode.objects.filter(
            **{field_name: value}
        ).first()

        if obj:
            return obj

        # Case insensitive fallback
        return PostalCode.objects.filter(
            **{f"{field_name}__iexact": value}
        ).first()


    # =====================================================
    # BEFORE IMPORT ROW
    # =====================================================

    def before_import_row(
        self,
        row,
        **kwargs
    ):
        """
        CSV row import hone se pehle data clean karega.
        """

        # =================================================
        # PHONE CLEAN
        # =================================================

        phone = row.get("phone")

        if phone:
            row["phone"] = clean_phone_last10(phone)

        # =================================================
        # CITY TEXT NORMALIZATION
        # =================================================

        if not row.get("city"):

            if row.get("city_name"):
                row["city"] = row.get("city_name")

            elif row.get("city_text"):
                row["city"] = row.get("city_text")


        # =================================================
        # LOCALITY NORMALIZATION
        # =================================================

        if not row.get("locality"):

            if row.get("locality_name"):
                row["locality"] = row.get("locality_name")


        # =================================================
        # AREA NORMALIZATION
        # =================================================

        if not row.get("area"):

            if row.get("area_name"):
                row["area"] = row.get("area_name")

            elif row.get("sub_locality"):
                row["area"] = row.get("sub_locality")


        # =================================================
        # POSTAL CODE NORMALIZATION
        # =================================================

        if not row.get("postal_code"):

            if row.get("postal_code_text"):
                row["postal_code"] = row.get(
                    "postal_code_text"
                )

            elif row.get("pincode"):
                row["postal_code"] = row.get(
                    "pincode"
                )


    # =====================================================
    # AFTER IMPORT INSTANCE
    # =====================================================

    def after_import_instance(
        self,
        instance,
        new,
        row_number=None,
        **kwargs
    ):
        """
        CSV ke text location values ko actual FK objects
        mein convert karta hai.
        """

        # =================================================
        # CITY
        # =================================================

        city_name = (
            row_value(
                kwargs.get("row"),
                "city"
            )
        )

        if not city_name:
            city_name = getattr(
                instance,
                "city_text",
                None
            )

        city_obj = self.get_location(
            city_name,
            LocationType.DISTRICT_CITY,
        )

        if city_obj:
            instance.city = city_obj


        # =================================================
        # LOCALITY
        # =================================================

        locality_name = row_value(
            kwargs.get("row"),
            "locality"
        )

        locality_obj = None

        if locality_name:

            locality_obj = self.get_location(
                locality_name,
                LocationType.LOCALITY_AREA,
                parent=city_obj,
            )

        if locality_obj:
            instance.locality = locality_obj


        # =================================================
        # AREA
        # =================================================

        area_name = row_value(
            kwargs.get("row"),
            "area"
        )

        area_obj = None

        if area_name:

            area_obj = self.get_location(
                area_name,
                LocationType.SUBLOCALITY_AREA,
                parent=locality_obj,
            )

        if area_obj:
            instance.area = area_obj


        # =================================================
        # POSTAL CODE
        # =================================================

        postal_value = row_value(
            kwargs.get("row"),
            "postal_code"
        )

        if not postal_value:

            postal_value = getattr(
                instance,
                "postal_code_text",
                None
            )

        postal_obj = self.get_postal_code(
            postal_value
        )

        if postal_obj:
            instance.postal_code = postal_obj


    # =====================================================
    # BEFORE SAVE INSTANCE
    # =====================================================

    def before_save_instance(
        self,
        instance,
        row,
        **kwargs
    ):
        """
        Save se pehle final data cleaning.
        """

        # ---------------------------------------------
        # Phone
        # ---------------------------------------------

        if instance.phone:

            instance.phone = clean_phone_last10(
                instance.phone
            )

        # ---------------------------------------------
        # Name
        # ---------------------------------------------

        if instance.name:

            instance.name = str(
                instance.name
            ).strip()

        # ---------------------------------------------
        # Website
        # ---------------------------------------------

        if instance.website:

            instance.website = str(
                instance.website
            ).strip()


# =========================================================
# SAFE ROW VALUE
# =========================================================

def row_value(row, key):
    """
    Tab safe value return karta hai jab row None ho.
    """

    if not row:
        return None

    value = row.get(key)

    if value is None:
        return None

    value = str(value).strip()

    if value in (
        "",
        "-",
        "--",
        "None",
        "null",
    ):
        return None

    return value



class RefrenseResource(resources.ModelResource):

    class Meta:

        model = Refrense

        # ID database me automatically generate hoga
        import_id_fields = ("contact_no",)

        skip_unchanged = True
        report_skipped = True

        fields = (
            "id",

            "status",
            "assigned_to",

            "refrense_name",

            "city",
            "locality",
            "area",

            "address",
            "description",

            "contact_no",
            "other_no",
            "email",
            "website",
            "google_map",

            "rating",
            "reviews_count",
            "business_status_raw",

            "logo",

            "is_verified",
            "is_featured",

            "slug",

            "created_at",
            "updated_at",
        )