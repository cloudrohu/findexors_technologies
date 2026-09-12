import re

from django.conf import settings
from django.db import models, transaction
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from apps.core.models import BaseModel
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
    Phone number ko clean karta hai.

    Example:
        +91 70435 72272
        +91-70435-72272
        (91) 70435 72272

    Result:
        7043572272
    """

    if not phone:
        return None

    phone = str(phone).strip()

    # +, space, -, (, ), etc. remove
    digits = re.sub(r"\D", "", phone)

    # Last 10 digits only
    if len(digits) >= 10:
        return digits[-10:]

    return digits

# REFRENSE
# =========================================================

class Refrense(BaseModel):

    # =====================================================
    # CUSTOM ID
    # =====================================================

    id = models.CharField(
        primary_key=True,
        max_length=10,
        editable=False,
        unique=True,
        db_index=True,
    )

    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("FollowUp", "Follow Up"),
        ("Not_received", "Not Received"),
        ("Not Interested", "Not Interested"),
        ("They Will Connect", "They Will Connect"),
        ("Call later", "Call later"),
        ("Call Tomorrow", "Call Tomorrow"),
        ("Switched Off", "Switched Off"),
        ("Invalid Number", "Invalid Number"),
        ("Meeting_FollowUp", "Meeting-Follow Up"),
    ]

    # =====================================================
    # STATUS
    # =====================================================

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New",
        db_index=True,
    )

    # =====================================================
    # ASSIGNED USER
    # =====================================================

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_refrenses",
    )

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    refrense_name = models.CharField(
        max_length=150,
    )

    # =====================================================
    # LOCATION
    # =====================================================

    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="refrense_city",
        limit_choices_to={
            "location_type": LocationType.DISTRICT_CITY,
        },
        null=True,
        blank=True,
    )

    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="refrense_locality",
        limit_choices_to={
            "location_type": LocationType.LOCALITY_AREA,
        },
        null=True,
        blank=True,
    )

    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="refrense_area",
        limit_choices_to={
            "location_type": LocationType.SUBLOCALITY_AREA,
        },
        null=True,
        blank=True,
    )

    address = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    # =====================================================
    # CONTACT
    # =====================================================

    contact_no = models.CharField(
        max_length=16,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )

    other_no = models.CharField(
        max_length=16,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    google_map = models.TextField(
        blank=True,
        null=True,
    )

    # =====================================================
    # GOOGLE INFORMATION
    # =====================================================

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )

    reviews_count = models.IntegerField(
        null=True,
        blank=True,
    )

    business_status_raw = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    # =====================================================
    # IMAGE
    # =====================================================

    logo = models.ImageField(
        upload_to="refrense/logo/",
        blank=True,
        null=True,
    )

    # =====================================================
    # VERIFICATION / FEATURED
    # =====================================================

    is_verified = models.BooleanField(
        default=False,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    # =====================================================
    # SLUG
    # =====================================================

    slug = models.SlugField(
        max_length=500,
        blank=True,
        null=True,
        db_index=True,
    )

    # =====================================================
    # LOGO PREVIEW
    # =====================================================

    def logo_preview(self):

        if self.logo:
            return mark_safe(
                f'<img src="{self.logo.url}" '
                f'width="60" '
                f'style="border-radius:6px;" />'
            )

        return "No Image"

    logo_preview.short_description = "Logo"

    # =====================================================
    # GENERATE ID
    # =====================================================

    def generate_id(self):

        last_record = (
            Refrense.objects
            .filter(id__startswith="RF")
            .order_by("-id")
            .first()
        )

        if not last_record:
            number = 1
        else:
            try:
                number = int(last_record.id[2:]) + 1
            except (ValueError, TypeError):
                number = 1

        return f"RF{number:07d}"

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        # -----------------------------------------
        # ID
        # -----------------------------------------

        if not self.id:
            self.id = self.generate_id()

        # -----------------------------------------
        # CLEAN CONTACT NUMBER
        # -----------------------------------------

        if self.contact_no:
            self.contact_no = clean_phone_last10(
                self.contact_no
            )

        # -----------------------------------------
        # CLEAN OTHER NUMBER
        # -----------------------------------------

        if self.other_no:
            self.other_no = clean_phone_last10(
                self.other_no
            )

        # -----------------------------------------
        # NEW RECORD
        # -----------------------------------------

        is_new = self._state.adding

        super().save(*args, **kwargs)

        # -----------------------------------------
        # SLUG
        # -----------------------------------------

        if is_new and not self.slug:

            self.slug = (
                f"{slugify(self.refrense_name)}-{self.id}"
            )

            super().save(
                update_fields=["slug"]
            )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):
        return f"{self.id} - {self.refrense_name}"

    # =====================================================
    # META
    # =====================================================

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Refrense"
        verbose_name_plural = "4. Refrenses"



# Apne actual imports ke according adjust karo
# from utility.models import Location, LocationType, PostalCode


class Realty(BaseModel):

    # =========================================================
    # CUSTOM ID
    # =========================================================
    # Example:
    # re0000001
    # re0000002
    # re0000003
    # =========================================================

    id = models.CharField(
        max_length=20,
        primary_key=True,
        editable=False,
        db_index=True,
    )

    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    name = models.CharField(
        max_length=255,
    )

    name_for_emails = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    # =========================================================
    # LOCATION
    # =========================================================

    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="realty_city",
        limit_choices_to={
            "location_type": LocationType.DISTRICT_CITY,
        },
        null=True,
        blank=True,
    )

    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="realty_locality",
        limit_choices_to={
            "location_type": LocationType.LOCALITY_AREA,
        },
        null=True,
        blank=True,
    )

    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="realty_area",
        limit_choices_to={
            "location_type": LocationType.SUBLOCALITY_AREA,
        },
        null=True,
        blank=True,
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        related_name="realty_postal_code",
        null=True,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    # =========================================================
    # ORIGINAL GOOGLE FIELDS
    # =========================================================

    category_text = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    type = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
    )

    website = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    street = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    city_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    state = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    postal_code_text = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
    )

    country = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
    )

    reviews = models.IntegerField(
        blank=True,
        null=True,
    )

    place_id = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )

    google_id = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        db_index=True,
    )

    cid = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        db_index=True,
    )

    business_status = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    working_hours = models.TextField(
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    about = models.TextField(
        blank=True,
        null=True,
    )

    logo = models.URLField(
        blank=True,
        null=True,
    )

    # =========================================================
    # STATUS
    # =========================================================

    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("Follow Up", "Follow Up"),
        ("Not Received", "Not Received"),
        ("Not Interested", "Not Interested"),
        ("They Will Connect", "They Will Connect"),
        ("Call later", "Call later"),
        ("Call Tomorrow", "Call Tomorrow"),
        ("Switched Off", "Switched Off"),
        ("Invalid Number", "Invalid Number"),
        ("Send Ditails", "Send Ditails"),
        ("Deal Done", "Deal Done"),
    ]

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New",
        db_index=True,
    )

    # =========================================================
    # ASSIGNED USER
    # =========================================================

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_realty",
    )

    # =========================================================
    # VERIFICATION / FEATURED
    # =========================================================

    is_verified = models.BooleanField(
        default=False,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    # =========================================================
    # SLUG
    # =========================================================

    slug = models.SlugField(
        max_length=500,
        blank=True,
        null=True,
        db_index=True,
    )

    # =========================================================
    # SAVE
    # =========================================================

    def save(self, *args, **kwargs):

        # -----------------------------------------------------
        # CLEAN PHONE
        # -----------------------------------------------------
        if self.phone:
            self.phone = clean_phone_last10(self.phone)

        # -----------------------------------------------------
        # NEW RECORD
        # -----------------------------------------------------
        is_new = not self.pk

        # -----------------------------------------------------
        # GENERATE CUSTOM REALTY ID
        # -----------------------------------------------------
        if is_new and not self.id:

            last_id = (
                Realty.objects
                .filter(id__startswith="re")
                .order_by("-id")
                .values_list("id", flat=True)
                .first()
            )

            if last_id:

                match = re.search(
                    r"(\d+)$",
                    last_id
                )

                if match:
                    next_number = (
                        int(match.group(1)) + 1
                    )
                else:
                    next_number = 1

            else:
                next_number = 1

            self.id = f"re{next_number:07d}"

        # -----------------------------------------------------
        # FIRST SAVE
        # -----------------------------------------------------

        super().save(*args, **kwargs)

        # -----------------------------------------------------
        # SLUG
        # -----------------------------------------------------

        if not self.slug:

            self.slug = (
                f"{slugify(self.name)}-{self.id}"
            )

            super().save(
                update_fields=["slug"]
            )

    # =========================================================
    # STRING
    # =========================================================

    def __str__(self):
        return (
            f"{self.name} "
            f"({self.city_text or '-'})"
        )

    # =========================================================
    # META
    # =========================================================

    class Meta:

        verbose_name = "Realty"

        verbose_name_plural = "0. Realty"

        ordering = [
            "-created_at"
        ]

# =========================================================
# INTERIOR
# =========================================================

class Interior(BaseModel):

    # =========================================================
    # CUSTOM ID
    # =========================================================
    # Example:
    # in0000001
    # in0000002
    # in0000003
    # =========================================================
    id = models.CharField(
        max_length=20,
        primary_key=True,
        editable=False,
        db_index=True,
    )

    # =========================================================
    # BASIC INFORMATION
    # =========================================================
    name = models.CharField(
        max_length=255,
    )

    name_for_emails = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    # =========================================================
    # LOCATION
    # =========================================================
    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="interior_city",
        limit_choices_to={
            "location_type": LocationType.DISTRICT_CITY,
        },
        null=True,
        blank=True,
    )

    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="interior_locality",
        limit_choices_to={
            "location_type": LocationType.LOCALITY_AREA,
        },
        null=True,
        blank=True,
    )

    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="interior_area",
        limit_choices_to={
            "location_type": LocationType.SUBLOCALITY_AREA,
        },
        null=True,
        blank=True,
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        related_name="interior_postal_code",
        null=True,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    # =========================================================
    # ORIGINAL GOOGLE FIELDS
    # =========================================================
    category_text = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    type = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
    )

    other_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
    )

    website = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    street = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    city_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    state = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    postal_code_text = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
    )

    country = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
    )

    reviews = models.IntegerField(
        blank=True,
        null=True,
    )

    place_id = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )

    google_id = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        db_index=True,
    )

    cid = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        db_index=True,
    )

    business_status = models.CharField(
        max_length=550,
        blank=True,
        null=True,
        db_index=True,
    )

    working_hours = models.TextField(
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    about = models.TextField(
        blank=True,
        null=True,
    )

    logo = models.URLField(
        blank=True,
        null=True,
    )

    # =========================================================
    # STATUS
    # =========================================================
    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("Follow Up", "Follow Up"),
        ("Not Received", "Not Received"),
        ("Not Interested", "Not Interested"),
        ("They Will Connect", "They Will Connect"),
        ("Call later", "Call later"),
        ("Call Tomorrow", "Call Tomorrow"),
        ("Switched Off", "Switched Off"),
        ("Invalid Number", "Invalid Number"),
        ("Send Ditails", "Send Ditails"),
        ("Deal Done", "Deal Done"),
    ]

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New",
        db_index=True,
    )

    # =========================================================
    # ASSIGNED USER
    # =========================================================
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_interiors",
    )

    # =========================================================
    # VERIFICATION / FEATURED
    # =========================================================
    is_verified = models.BooleanField(
        default=False,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    # =========================================================
    # SLUG
    # =========================================================
    slug = models.SlugField(
        max_length=500,
        blank=True,
        null=True,
        db_index=True,
    )

    # =========================================================
    # SAVE
    # =========================================================
    def save(self, *args, **kwargs):

        # -----------------------------------------------------
        # CLEAN PHONE
        # -----------------------------------------------------
        if self.phone:
            self.phone = clean_phone_last10(
                self.phone
            )

        # -----------------------------------------------------
        # CLEAN OTHER PHONE
        # -----------------------------------------------------
        if self.other_phone:
            self.other_phone = clean_phone_last10(
                self.other_phone
            )

        # -----------------------------------------------------
        # NEW RECORD
        # -----------------------------------------------------
        is_new = not self.pk

        # -----------------------------------------------------
        # GENERATE CUSTOM INTERIOR ID
        # -----------------------------------------------------
        if is_new and not self.id:

            last_id = (
                Interior.objects
                .filter(id__startswith="in")
                .order_by("-id")
                .values_list("id", flat=True)
                .first()
            )

            if last_id:
                match = re.search(
                    r"(\d+)$",
                    last_id
                )

                if match:
                    next_number = (
                        int(match.group(1)) + 1
                    )
                else:
                    next_number = 1

            else:
                next_number = 1

            self.id = f"in{next_number:07d}"

        # -----------------------------------------------------
        # FIRST SAVE
        # -----------------------------------------------------
        super().save(*args, **kwargs)

        # -----------------------------------------------------
        # SLUG
        # -----------------------------------------------------
        if not self.slug:

            self.slug = (
                f"{slugify(self.name)}-{self.id}"
            )

            super().save(
                update_fields=["slug"]
            )

    # =========================================================
    # STRING
    # =========================================================
    def __str__(self):

        return (
            f"{self.name} "
            f"({self.city_text or '-'})"
        )

    # =========================================================
    # META
    # =========================================================
    class Meta:

        verbose_name = "Interior"

        verbose_name_plural = "1. Interiors"

        ordering = [
            "-created_at"
        ]

# =========================================================
# COMMENT
# =========================================================

class Comment(BaseModel):

    realty = models.ForeignKey(
        Realty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments",
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):

        if self.realty:
            return self.realty.name

        return "Comment"


# =========================================================
# VOICE RECORDING
# =========================================================

class VoiceRecording(BaseModel):

    realty = models.ForeignKey(
        Realty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="voice_recordings",
    )

    file = models.FileField(
        upload_to="voice_recordings/",
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="realty_voice_recordings",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Voice Recording"
        verbose_name_plural = "Voice Recordings"

    def __str__(self):

        if self.realty:
            return f"{self.realty.name} Voice"

        return f"Voice {self.pk}"


# =========================================================
# VISIT
# =========================================================

class Visit(BaseModel):

    realty = models.ForeignKey(
        Realty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="visits",
    )

    visit_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_realty_visits",
    )

    class Meta:
        ordering = ["-visit_date"]
        verbose_name = "Visit"
        verbose_name_plural = "Visits"

    def __str__(self):

        if self.realty:
            return f"{self.realty.name} - Visit"

        return f"Visit {self.pk}"


# =========================================================
# FOLLOWUP
# =========================================================

class Followup(BaseModel):

    FOLLOWUP_STATUS_CHOICES = [
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    # =====================================================
    # REALTY
    # =====================================================

    realty = models.OneToOneField(
        Realty,
        on_delete=models.CASCADE,
        related_name="followup",
    )

    # =====================================================
    # FOLLOWUP NUMBER
    # =====================================================

    followup_no = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    # =====================================================
    # STATUS
    # =====================================================

    status = models.CharField(
        max_length=25,
        choices=FOLLOWUP_STATUS_CHOICES,
        default="New Followup",
    )

    # =====================================================
    # FOLLOWUP DATE
    # =====================================================

    followup_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    # =====================================================
    # ASSIGNED USER
    # =====================================================

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_realty_followups",
    )

    # =====================================================
    # COMMENT
    # =====================================================

    comment = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        if not self.followup_no:

            with transaction.atomic():

                last = (
                    Followup.objects
                    .select_for_update()
                    .order_by("-followup_no")
                    .first()
                )

                number = (
                    int(last.followup_no[2:]) + 1
                    if last and last.followup_no
                    else 1
                )

                self.followup_no = f"RF{number:06d}"

        super().save(*args, **kwargs)

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):
        return f"{self.followup_no} - {self.status}"

    # =====================================================
    # META
    # =====================================================

    class Meta:
        ordering = ("-followup_date",)
        verbose_name = "Follow Up"
        verbose_name_plural = "2. Follow Ups"


# =========================================================
# MEETING
# =========================================================

class Meeting(BaseModel):

    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    # =====================================================
    # REALTY
    # =====================================================

    realty = models.OneToOneField(
        Realty,
        on_delete=models.CASCADE,
        related_name="meeting",
    )

    # =====================================================
    # MEETING NUMBER
    # =====================================================

    meeting_no = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    # =====================================================
    # STATUS
    # =====================================================

    status = models.CharField(
        max_length=25,
        choices=MEETING_STATUS_CHOICES,
        default="New Meeting",
    )

    # =====================================================
    # MEETING DATE
    # =====================================================

    meeting_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    # =====================================================
    # ASSIGNED USER
    # =====================================================

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_realty_meetings",
    )

    # =====================================================
    # COMMENT
    # =====================================================

    comment = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        if not self.meeting_no:

            with transaction.atomic():

                last = (
                    Meeting.objects
                    .select_for_update()
                    .order_by("-meeting_no")
                    .first()
                )

                number = (
                    int(last.meeting_no[2:]) + 1
                    if last and last.meeting_no
                    else 1
                )

                self.meeting_no = f"RM{number:06d}"

        super().save(*args, **kwargs)

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):
        return f"{self.meeting_no} - {self.status}"

    # =====================================================
    # META
    # =====================================================

    class Meta:
        ordering = ("-meeting_date",)
        verbose_name = "Meeting"
        verbose_name_plural = "1. Meetings"