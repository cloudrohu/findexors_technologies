import re

from import_export import resources

from .models import Realty, Refrense,Interior



from import_export import fields
from import_export.widgets import CharWidget
# =========================================================
# PHONE NUMBER EXTRACTOR
# =========================================================

def extract_phone_numbers(value):
    """
    Multiple phone numbers ko identify karta hai.

    Examples:

        9876543210
        -> ["9876543210"]

        +91 96992 45556
        -> ["9699245556"]

        9699245556, 9833903951
        -> ["9699245556", "9833903951"]

        9699245556 / 9833903951
        -> ["9699245556", "9833903951"]
    """

    if not value:
        return []

    value = str(value).strip()

    # -----------------------------------------------------
    # Extension remove
    # -----------------------------------------------------

    value = re.sub(
        r"(?i)(ext|extension)\.?\s*\d+",
        "",
        value,
    )

    # -----------------------------------------------------
    # Common separators
    # -----------------------------------------------------

    parts = re.split(
        r"[,;/|&\n]+",
        value,
    )

    numbers = []

    for part in parts:

        part = part.strip()

        if not part:
            continue

        # -------------------------------------------------
        # Remove all non-digits
        # -------------------------------------------------

        digits = re.sub(
            r"\D",
            "",
            part,
        )

        if len(digits) < 10:
            continue

        # -------------------------------------------------
        # Last 10 digits
        # -------------------------------------------------

        number = digits[-10:]

        # -------------------------------------------------
        # Indian mobile number
        # -------------------------------------------------

        if (
            len(number) == 10
            and number[0] in "6789"
        ):

            if number not in numbers:
                numbers.append(number)

    return numbers


# =========================================================
# CLEAN SINGLE PHONE
# =========================================================

def clean_phone_last10(phone):

    if not phone:
        return None

    numbers = extract_phone_numbers(phone)

    if numbers:
        return numbers[0]

    return None


# =========================================================
# NORMALIZE NAME
# =========================================================

def normalize_name(name):

    if not name:
        return ""

    name = str(name).strip().lower()

    # Multiple spaces remove
    name = re.sub(
        r"\s+",
        " ",
        name,
    )

    return name


# =========================================================
# ADD UNIQUE PHONE
# =========================================================

def add_unique_phone(phone_list, number):

    if not number:
        return

    number = clean_phone_last10(number)

    if not number:
        return

    if number not in phone_list:
        phone_list.append(number)


# =========================================================
# REALTY RESOURCE
# =========================================================

class RealtyResource(resources.ModelResource):

    class Meta:

        model = Realty

        # Existing Realty ko place_id se identify karega
        import_id_fields = (
            "place_id",
        )

        skip_unchanged = True
        report_skipped = True

        fields = (

            # -------------------------------------------------
            # BASIC
            # -------------------------------------------------

            "name",
            "name_for_emails",

            # -------------------------------------------------
            # LOCATION
            # -------------------------------------------------

            "city",
            "locality",
            "area",
            "postal_code",

            "address",

            # -------------------------------------------------
            # GOOGLE
            # -------------------------------------------------

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

            # -------------------------------------------------
            # STATUS
            # -------------------------------------------------

            "status",
            "assigned_to",

            "is_verified",
            "is_featured",
            "is_active",
        )

    # =====================================================
    # REALTY PHONE CLEAN
    # =====================================================

    def before_import_row(
        self,
        row,
        **kwargs,
    ):

        phone = row.get("phone")

        numbers = extract_phone_numbers(
            phone
        )

        if numbers:

            row["phone"] = numbers[0]

        else:

            row["phone"] = ""




# =========================================================
# PHONE CLEANER
# =========================================================

def clean_phone_last10(phone):

    """
    Examples:

    +91 98765 43210  -> 9876543210
    919876543210     -> 9876543210
    98765-43210      -> 9876543210
    """

    if not phone:
        return None

    phone = str(phone).strip()

    digits = re.sub(r"\D", "", phone)

    if len(digits) >= 10:
        return digits[-10:]

    return digits


# =========================================================
# INTERIOR RESOURCE
# =========================================================




class InteriorResource(resources.ModelResource):

    # =====================================================
    # CSV -> MODEL FIELD MAPPING
    # =====================================================

    name = fields.Field(
        column_name="name",
        attribute="name",
    )

    name_for_emails = fields.Field(
        column_name="name_for_emails",
        attribute="name_for_emails",
    )

    category_text = fields.Field(
        column_name="category",
        attribute="category_text",
    )

    type = fields.Field(
        column_name="type",
        attribute="type",
    )

    phone = fields.Field(
        column_name="phone",
        attribute="phone",
    )

    website = fields.Field(
        column_name="website",
        attribute="website",
    )

    address = fields.Field(
        column_name="address",
        attribute="address",
    )

    street = fields.Field(
        column_name="street",
        attribute="street",
    )

    city_text = fields.Field(
        column_name="city",
        attribute="city_text",
    )

    state = fields.Field(
        column_name="state",
        attribute="state",
    )

    postal_code_text = fields.Field(
        column_name="postal_code",
        attribute="postal_code_text",
    )

    country = fields.Field(
        column_name="country",
        attribute="country",
    )

    latitude = fields.Field(
        column_name="latitude",
        attribute="latitude",
    )

    longitude = fields.Field(
        column_name="longitude",
        attribute="longitude",
    )

    rating = fields.Field(
        column_name="rating",
        attribute="rating",
    )

    reviews = fields.Field(
        column_name="reviews",
        attribute="reviews",
    )

    business_status = fields.Field(
        column_name="business_status",
        attribute="business_status",
    )

    working_hours = fields.Field(
        column_name="working_hours",
        attribute="working_hours",
    )

    description = fields.Field(
        column_name="description",
        attribute="description",
    )

    about = fields.Field(
        column_name="about",
        attribute="about",
    )

    logo = fields.Field(
        column_name="logo",
        attribute="logo",
    )

    place_id = fields.Field(
        column_name="place_id",
        attribute="place_id",
    )

    google_id = fields.Field(
        column_name="google_id",
        attribute="google_id",
    )

    cid = fields.Field(
        column_name="cid",
        attribute="cid",
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        model = Interior

        # -------------------------------------------------
        # IMPORTANT
        # -------------------------------------------------
        # ID CSV se nahi lena hai.
        # Model khud generate karega:
        #
        # in0000001
        # in0000002
        # in0000003
        # -------------------------------------------------

        exclude = (
            "id",
            "slug",
            "created_at",
            "updated_at",
            "is_active",
            "status",
            "assigned_to",
            "is_verified",
            "is_featured",
        )

        skip_unchanged = True

        report_skipped = True

    # =====================================================
    # BEFORE IMPORT ROW
    # =====================================================

    def before_import_row(self, row, **kwargs):

        # -------------------------------------------------
        # PHONE
        # -------------------------------------------------

        phone = row.get("phone")

        if phone:
            row["phone"] = clean_phone_last10(phone)

        # -------------------------------------------------
        # OTHER PHONE
        # -------------------------------------------------
        # Agar CSV mein future mein other_phone aaye
        # to automatically clean ho jayega.
        # -------------------------------------------------

        other_phone = row.get("other_phone")

        if other_phone:
            row["other_phone"] = clean_phone_last10(
                other_phone
            )

    # =====================================================
    # DUPLICATE PHONE CHECK
    # =====================================================

    def skip_row(
        self,
        instance,
        original,
        row,
        import_validation_errors=None,
    ):

        phone = clean_phone_last10(
            row.get("phone")
        )

        # -------------------------------------------------
        # PHONE EMPTY
        # -------------------------------------------------

        if not phone:
            return False

        # -------------------------------------------------
        # DATABASE DUPLICATE
        # -------------------------------------------------

        if Interior.objects.filter(
            phone=phone
        ).exists():

            return True

        # -------------------------------------------------
        # SAME CSV FILE DUPLICATE
        # -------------------------------------------------

        if not hasattr(
            self,
            "_import_phone_numbers"
        ):

            self._import_phone_numbers = set()

        if phone in self._import_phone_numbers:

            return True

        self._import_phone_numbers.add(phone)

        return False

    # =====================================================
    # BEFORE IMPORT
    # =====================================================

    def before_import(
        self,
        dataset,
        **kwargs
    ):

        self._import_phone_numbers = set()

        return super().before_import(
            dataset,
            **kwargs
        )




# =========================================================
# REFRENSE RESOURCE
# =========================================================

class RefrenseResource(resources.ModelResource):

    class Meta:

        model = Refrense

        # -------------------------------------------------
        # IMPORTANT
        # -------------------------------------------------
        # ID CSV se import nahi hoga.
        #
        # Model automatically:
        #
        # RF0000001
        # RF0000002
        # RF0000003
        #
        # generate karega.
        # -------------------------------------------------

        exclude = (
            "id",
            "slug",
        )

        skip_unchanged = True
        report_skipped = True

        fields = (

            # -------------------------------------------------
            # STATUS
            # -------------------------------------------------

            "status",
            "assigned_to",

            # -------------------------------------------------
            # BASIC
            # -------------------------------------------------

            "refrense_name",

            # -------------------------------------------------
            # LOCATION
            # -------------------------------------------------

            "city",
            "locality",
            "area",

            "address",
            "description",

            # -------------------------------------------------
            # CONTACT
            # -------------------------------------------------

            "contact_no",
            "other_no",

            "email",
            "website",
            "google_map",

            # -------------------------------------------------
            # GOOGLE
            # -------------------------------------------------

            "rating",
            "reviews_count",
            "business_status_raw",

            # -------------------------------------------------
            # IMAGE
            # -------------------------------------------------

            "logo",

            # -------------------------------------------------
            # FLAGS
            # -------------------------------------------------

            "is_verified",
            "is_featured",
            "is_active",
        )

    # =====================================================
    # BEFORE IMPORT
    # =====================================================

    def before_import(
        self,
        dataset,
        **kwargs,
    ):
        """
        Import hone se pehle CSV ki rows ko merge karta hai.

        Example:

        CSV:

        Kamal Nagdevin | 9699245556
        Kamal Nagdevin | 9833903951

        Convert hoga:

        Kamal Nagdevin | 9699245556 | 9833903951

        Isliye 2 database records nahi banenge.
        """

        # -------------------------------------------------
        # Already processed names
        # -------------------------------------------------

        processed = {}

        # -------------------------------------------------
        # Original rows ko list mein convert
        # -------------------------------------------------

        rows = list(dataset.dict)

        merged_rows = []

        for original_row in rows:

            # =================================================
            # NAME
            # =================================================

            name = original_row.get(
                "refrense_name"
            )

            normalized_name = normalize_name(
                name
            )

            # -------------------------------------------------
            # Agar name empty hai
            # -------------------------------------------------

            if not normalized_name:

                merged_rows.append(
                    original_row
                )

                continue

            # =================================================
            # ALL PHONE NUMBERS
            # =================================================

            phone_numbers = []

            # -------------------------------------------------
            # contact_no
            # -------------------------------------------------

            for number in extract_phone_numbers(
                original_row.get("contact_no")
            ):

                add_unique_phone(
                    phone_numbers,
                    number,
                )

            # -------------------------------------------------
            # other_no
            # -------------------------------------------------

            for number in extract_phone_numbers(
                original_row.get("other_no")
            ):

                add_unique_phone(
                    phone_numbers,
                    number,
                )

            # =================================================
            # FIRST TIME NAME
            # =================================================

            if normalized_name not in processed:

                new_row = dict(
                    original_row
                )

                # -------------------------------------------------
                # First number = contact_no
                # -------------------------------------------------

                if phone_numbers:

                    new_row["contact_no"] = (
                        phone_numbers[0]
                    )

                else:

                    new_row["contact_no"] = ""

                # -------------------------------------------------
                # Second number = other_no
                # -------------------------------------------------

                if len(phone_numbers) >= 2:

                    new_row["other_no"] = (
                        phone_numbers[1]
                    )

                else:

                    new_row["other_no"] = ""

                # -------------------------------------------------
                # Save index
                # -------------------------------------------------

                processed[
                    normalized_name
                ] = len(merged_rows)

                merged_rows.append(
                    new_row
                )

                continue

            # =================================================
            # SAME NAME ALREADY EXISTS
            # =================================================

            existing_index = processed[
                normalized_name
            ]

            existing_row = merged_rows[
                existing_index
            ]

            # =================================================
            # EXISTING PHONE NUMBERS
            # =================================================

            existing_numbers = []

            # -------------------------------------------------
            # Existing contact
            # -------------------------------------------------

            for number in extract_phone_numbers(
                existing_row.get("contact_no")
            ):

                add_unique_phone(
                    existing_numbers,
                    number,
                )

            # -------------------------------------------------
            # Existing other
            # -------------------------------------------------

            for number in extract_phone_numbers(
                existing_row.get("other_no")
            ):

                add_unique_phone(
                    existing_numbers,
                    number,
                )

            # =================================================
            # MERGE NEW NUMBERS
            # =================================================

            for number in phone_numbers:

                add_unique_phone(
                    existing_numbers,
                    number,
                )

            # =================================================
            # SET CONTACT NUMBER
            # =================================================

            if existing_numbers:

                existing_row["contact_no"] = (
                    existing_numbers[0]
                )

            else:

                existing_row["contact_no"] = ""

            # =================================================
            # SET OTHER NUMBER
            # =================================================

            if len(existing_numbers) >= 2:

                existing_row["other_no"] = (
                    existing_numbers[1]
                )

            else:

                existing_row["other_no"] = ""

            # =================================================
            # EMAIL
            # =================================================

            if (
                not existing_row.get("email")
                and original_row.get("email")
            ):

                existing_row["email"] = (
                    original_row.get("email")
                )

            # =================================================
            # WEBSITE
            # =================================================

            if (
                not existing_row.get("website")
                and original_row.get("website")
            ):

                existing_row["website"] = (
                    original_row.get("website")
                )

            # =================================================
            # ADDRESS
            # =================================================

            if (
                not existing_row.get("address")
                and original_row.get("address")
            ):

                existing_row["address"] = (
                    original_row.get("address")
                )

            # =================================================
            # DESCRIPTION
            # =================================================

            if (
                not existing_row.get("description")
                and original_row.get("description")
            ):

                existing_row["description"] = (
                    original_row.get("description")
                )

        # =====================================================
        # DATASET REBUILD
        # =====================================================

        if merged_rows:

            headers = dataset.headers

            dataset.wipe(
                headers=headers
            )

            for row in merged_rows:

                dataset.append(
                    [
                        row.get(
                            header,
                            "",
                        )
                        for header in headers
                    ]
                )

        # =====================================================
        # DUPLICATE CACHE
        # =====================================================

        self._import_contact_numbers = set()

        return super().before_import(
            dataset,
            **kwargs,
        )

    # =====================================================
    # BEFORE IMPORT ROW
    # =====================================================

    def before_import_row(
        self,
        row,
        **kwargs,
    ):
        """
        Individual row ke phone numbers clean karta hai.

        Example:

        contact_no:
            +91 96992 45556

        other_no:
            +91 98339 03951

        Result:

        contact_no = 9699245556
        other_no   = 9833903951
        """

        # =================================================
        # CONTACT NUMBERS
        # =================================================

        contact_numbers = extract_phone_numbers(
            row.get("contact_no")
        )

        # =================================================
        # OTHER NUMBERS
        # =================================================

        other_numbers = extract_phone_numbers(
            row.get("other_no")
        )

        # =================================================
        # ALL NUMBERS
        # =================================================

        all_numbers = []

        # Contact first
        for number in contact_numbers:

            add_unique_phone(
                all_numbers,
                number,
            )

        # Other second
        for number in other_numbers:

            add_unique_phone(
                all_numbers,
                number,
            )

        # =================================================
        # CONTACT NUMBER
        # =================================================

        if all_numbers:

            row["contact_no"] = (
                all_numbers[0]
            )

        else:

            row["contact_no"] = ""

        # =================================================
        # OTHER NUMBER
        # =================================================

        if len(all_numbers) >= 2:

            row["other_no"] = (
                all_numbers[1]
            )

        else:

            row["other_no"] = ""

    # =====================================================
    # SKIP ROW
    # =====================================================

    def skip_row(
        self,
        instance,
        original,
        row,
        import_validation_errors=None,
    ):
        """
        Duplicate contact number ko prevent karta hai.

        Database:

            RF0000001 | Kamal | 9699245556

        CSV:

            Kamal | 9699245556

        Duplicate hai -> skip.

        Same CSV:

            Kamal | 9699245556
            Kamal | 9699245556

        Duplicate hai -> ek hi record.
        """

        # =================================================
        # CONTACT
        # =================================================

        contact_no = clean_phone_last10(
            row.get("contact_no")
        )

        # =================================================
        # EMPTY CONTACT
        # =================================================

        if not contact_no:

            return False

        # =================================================
        # DATABASE DUPLICATE
        # =================================================

        existing = (
            Refrense.objects
            .filter(
                contact_no=contact_no
            )
            .first()
        )

        if existing:

            return True

        # =================================================
        # SAME IMPORT DUPLICATE
        # =================================================

        if contact_no in (
            self._import_contact_numbers
        ):

            return True

        self._import_contact_numbers.add(
            contact_no
        )

        return False