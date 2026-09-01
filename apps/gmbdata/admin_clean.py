from import_export import resources, fields

from .models import Realty

from apps.utility.models import (
    Location,
    LocationType,
    PostalCode,
)


# =========================================================
# REALTY RESOURCE
# =========================================================

class RealtyResource(resources.ModelResource):

    # =====================================================
    # CSV FIELD -> REALTY FIELD
    # =====================================================

    category_text = fields.Field(
        column_name="category",
        attribute="category_text",
    )

    city_text = fields.Field(
        column_name="city",
        attribute="city_text",
    )

    postal_code_text = fields.Field(
        column_name="postal_code",
        attribute="postal_code_text",
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        model = Realty

        # Existing record ko place_id se identify karega
        import_id_fields = (
            "place_id",
        )

        skip_unchanged = True
        report_skipped = True

        # =================================================
        # ONLY CSV DATA FIELDS
        # =================================================

        fields = (
            "name",
            "name_for_emails",

            "category_text",
            "type",

            "phone",
            "website",

            "address",
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

            "about",
            "description",

            "logo",
        )

    # =====================================================
    # LOCATION HELPERS
    # =====================================================

    def get_location(
        self,
        name,
        location_type,
        parent=None,
    ):
        """
        Location ko name + type + parent ke basis par
        find karta hai.
        """

        if not name:
            return None

        name = str(name).strip()

        if not name:
            return None

        queryset = Location.objects.filter(
            name__iexact=name,
            location_type=location_type,
        )

        if parent:
            queryset = queryset.filter(
                parent=parent
            )
        else:
            queryset = queryset.filter(
                parent__isnull=True
            )

        return queryset.first()

    # =====================================================
    # CREATE LOCATION
    # =====================================================

    def create_location(
        self,
        name,
        location_type,
        parent=None,
    ):
        """
        Location create karega agar already available nahi hai.
        """

        if not name:
            return None

        name = str(name).strip()

        if not name:
            return None

        location = self.get_location(
            name=name,
            location_type=location_type,
            parent=parent,
        )

        if location:
            return location

        return Location.objects.create(
            name=name,
            location_type=location_type,
            parent=parent,
        )

    # =====================================================
    # POSTAL CODE
    # =====================================================

    def get_postal_code(
        self,
        code,
        location=None,
    ):
        """
        PostalCode ko code ke basis par find/create karta hai.
        """

        if not code:
            return None

        code = str(code).strip()

        if not code:
            return None

        postal = PostalCode.objects.filter(
            code=code
        ).first()

        if postal:
            return postal

        # PostalCode ko location chahiye.
        if not location:
            return None

        return PostalCode.objects.create(
            code=code,
            location=location,
        )

    # =====================================================
    # BEFORE IMPORT ROW
    # =====================================================

    def before_import_row(
        self,
        row,
        **kwargs,
    ):

        # -------------------------------------------------
        # PHONE CLEAN
        # -------------------------------------------------

        phone = str(
            row.get("phone") or ""
        ).strip()

        if phone:
            row["phone"] = phone

        # -------------------------------------------------
        # CITY
        # CSV:
        # city
        # Realty:
        # city_text
        # -------------------------------------------------

        if row.get("city"):
            row["city_text"] = str(
                row.get("city")
            ).strip()

        # -------------------------------------------------
        # CATEGORY
        # CSV:
        # category
        # Realty:
        # category_text
        # -------------------------------------------------

        if row.get("category"):
            row["category_text"] = str(
                row.get("category")
            ).strip()

        # -------------------------------------------------
        # POSTAL CODE
        # CSV:
        # postal_code
        # Realty:
        # postal_code_text
        # -------------------------------------------------

        if row.get("postal_code"):
            row["postal_code_text"] = str(
                row.get("postal_code")
            ).strip()

    # =====================================================
    # AFTER IMPORT INSTANCE
    # =====================================================

    def after_import_instance(
        self,
        instance,
        new,
        row_number=None,
        **kwargs,
    ):

        row = kwargs.get("row")

        if not row:
            return

        # =================================================
        # COUNTRY
        # =================================================

        country_name = str(
            row.get("country") or ""
        ).strip()

        country = None

        if country_name:

            country = self.create_location(
                name=country_name,
                location_type=LocationType.COUNTRY,
            )

        # =================================================
        # STATE
        # =================================================

        state_name = str(
            row.get("state") or ""
        ).strip()

        state = None

        if state_name:

            state = self.create_location(
                name=state_name,
                location_type=LocationType.STATE,
                parent=country,
            )

        # =================================================
        # CITY
        # =================================================

        city_name = str(
            row.get("city") or ""
        ).strip()

        city = None

        if city_name:

            city = self.create_location(
                name=city_name,
                location_type=LocationType.DISTRICT_CITY,
                parent=state,
            )

            instance.city = city

        # =================================================
        # LOCALITY
        # =================================================
        #
        # CSV mein separate locality column nahi hai.
        #
        # Google CSV ka "county" available hai.
        # Isko Locality/Area ke roop mein use kar rahe hain.
        #
        # =================================================

        locality_name = str(
            row.get("county") or ""
        ).strip()

        locality = None

        if locality_name and city:

            locality = self.create_location(
                name=locality_name,
                location_type=LocationType.LOCALITY_AREA,
                parent=city,
            )

            instance.locality = locality

        # =================================================
        # AREA
        # =================================================
        #
        # CSV mein separate area/sub-locality field nahi hai.
        # Isliye area ko automatically guess nahi karenge.
        #
        # =================================================

        instance.area = None

        # =================================================
        # POSTAL CODE
        # =================================================

        postal_code = str(
            row.get("postal_code") or ""
        ).strip()

        if postal_code:

            # PostalCode ko locality chahiye.
            postal_location = locality

            postal_obj = self.get_postal_code(
                code=postal_code,
                location=postal_location,
            )

            if postal_obj:
                instance.postal_code = postal_obj

        # =================================================
        # SAVE
        # =================================================

        instance.save()