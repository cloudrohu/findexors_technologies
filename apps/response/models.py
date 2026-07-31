import re
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.db import transaction

from apps.core.models import BaseModel

from apps.utility.models import (
    Location,
    PostalCode,
    LocationType,
    RequirementType,
)
from apps.companies.models import (
    CompanyCategory,
    
)
# ✅ Phone Cleaner (Save Time): last 10 digits only
def clean_phone_last10(phone: str):
    """
    ✅ Keeps field max_length same (16),
    but when saving returns ONLY last 10 digits.
    Works with +91, spaces, dashes, etc.
    """
    if not phone:
        return None

    phone = str(phone).strip()

    # ✅ keep only digits
    digits = re.sub(r"\D", "", phone)

    # ✅ return last 10 digits if available
    if len(digits) >= 10:
        return digits[-10:]

    return digits


# =======================
#  Staff
# =======================
class Response(BaseModel):

    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("Follow_Up", "Follow Up"),
        ("Meeting_FollowUp", "Meeting / Follow Up"),
        ("Not_received", "Not Received"),
        ("Software_company", "Software Company"),
        ("For_job", "For Job"),
        ("Training", "Training"),
        ("Fake_lead", "Fake Lead"),
        ("Deal_close", "Deal Close"),
    ]

    LEAD_SOURCE_CHOICES = [
        ("instagram", "Instagram Ads"),
        ("facebook", "Facebook Ads"),
        ("google", "Google Ads"),
        ("website", "Website"),
        ("whatsapp", "WhatsApp"),
        ("Just Dial", "Just Dial"),
        ("manual", "Manual"),
    ]

    lead_source = models.CharField(
        max_length=20,
        choices=LEAD_SOURCE_CHOICES,
        default="manual",
        db_index=True,
    )

    # ===============================
    # WhatsApp Tracking
    # ===============================

    whatsapp_welcome_sent = models.BooleanField(default=False)
    whatsapp_followup_1_sent = models.BooleanField(default=False)
    whatsapp_followup_2_sent = models.BooleanField(default=False)

    # ===============================
    # Conversion
    # ===============================

    is_converted = models.BooleanField(default=False)
    converted_at = models.DateTimeField(blank=True, null=True)

    # ===============================
    # Status
    # ===============================

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New",
        db_index=True,
    )

    # ===============================
    # Basic Details
    # ===============================

    response_no = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    contact_no = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
    )

    contact_persone = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    business_name = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_response",
    )

    business_category = models.ForeignKey(
        CompanyCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    requirement_types = models.ManyToManyField(
        RequirementType,
        blank=True,
        related_name="responses",
    )

    # ===============================
    # Address
    # ===============================

    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="response_city",
        limit_choices_to={
            "location_type": LocationType.DISTRICT_CITY,
        },
        null=True,
        blank=True,
    )

    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="response_locality",
        limit_choices_to={
            "location_type": LocationType.LOCALITY_AREA,
        },
        null=True,
        blank=True,
    )

    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="response_area",
        limit_choices_to={
            "location_type": LocationType.SUBLOCALITY_AREA,
        },
        null=True,
        blank=True,
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        related_name="response",
        null=True,
        blank=True,
    )

    address = models.TextField(blank=True)

    # ===========================================
    # AUTO STATUS REFRESH
    # ===========================================
    def refresh_status(self):

        has_meeting = Meeting.objects.filter(response=self).exists()
        has_followup = Followup.objects.filter(response=self).exists()

        if has_meeting and has_followup:
            status = "Meeting_FollowUp"

        elif has_meeting:
            status = "Meeting"

        elif has_followup:
            status = "Follow_Up"

        else:
            status = "New"

        self.status = status
        self.save(update_fields=["status"])
    # ===========================================
    # SAVE
    # ===========================================

    def save(self, *args, **kwargs):

        # Clean phone number
        if self.contact_no:
            self.contact_no = clean_phone_last10(self.contact_no)

        # Generate Response Number
        if not self.response_no:

            with transaction.atomic():

                last = (
                    Response.objects
                    .select_for_update()
                    .order_by("-response_no")
                    .first()
                )

                if last and last.response_no:
                    number = int(last.response_no[1:]) + 1
                else:
                    number = 1

                self.response_no = f"R{number:06d}"

        # Conversion Timestamp
        if self.is_converted:

            if not self.converted_at:
                self.converted_at = timezone.now()

        else:
            self.converted_at = None

        super().save(*args, **kwargs)

    # ===========================================
    # STRING
    # ===========================================

    def __str__(self):
        return f"{self.response_no} - {self.contact_no or 'No Number'}"

    # ===========================================
    # META
    # ===========================================

    class Meta:

        ordering = ("-created_at",)

        verbose_name = "Response"
        verbose_name_plural = "0. Responses"

        indexes = [
            models.Index(fields=["response_no"]),
            models.Index(fields=["contact_no"]),
            models.Index(fields=["status"]),
            models.Index(fields=["lead_source"]),
            models.Index(fields=["is_converted"]),
        ]

class Meeting(BaseModel):

    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    response = models.OneToOneField(
        Response,
        on_delete=models.CASCADE,
        related_name="meeting",
    )

    meeting_no = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    status = models.CharField(
        max_length=25,
        choices=MEETING_STATUS_CHOICES,
        default="New Meeting",
    )

    meeting_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_response_meetings",
    )

    comment = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    # ==========================================
    # SAVE
    # ==========================================

    def save(self, *args, **kwargs):

        # Generate Meeting Number
        if not self.meeting_no:

            with transaction.atomic():

                last = (
                    Meeting.objects
                    .select_for_update()
                    .order_by("-meeting_no")
                    .first()
                )

                if last and last.meeting_no:
                    number = int(last.meeting_no[2:]) + 1
                else:
                    number = 1

                self.meeting_no = f"RM{number:06d}"

        super().save(*args, **kwargs)

        # Refresh Response Status
        self.response.refresh_status()

        # Deal Done
        if self.status == "Deal Done":

            Response.objects.filter(pk=self.response_id).update(
                status="Deal_close",
                is_converted=True,
                converted_at=timezone.now(),
            )

    # ==========================================
    # DELETE
    # ==========================================

    def delete(self, *args, **kwargs):

        response = self.response

        super().delete(*args, **kwargs)

        response.refresh_status()

    # ==========================================
    # STRING
    # ==========================================

    def __str__(self):
        return f"{self.meeting_no} - {self.status}"

    # ==========================================
    # META
    # ==========================================

    class Meta:
        ordering = ("-meeting_date",)
        verbose_name = "Meeting"
        verbose_name_plural = "1. Meetings"

        indexes = [
            models.Index(fields=["meeting_no"]),
            models.Index(fields=["meeting_date"]),
            models.Index(fields=["status"]),
        ]


class Followup(BaseModel):

    FOLLOWUP_STATUS_CHOICES = [
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    response = models.OneToOneField(
        Response,
        on_delete=models.CASCADE,
        related_name="followup",
    )

    followup_no = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    status = models.CharField(
        max_length=25,
        choices=FOLLOWUP_STATUS_CHOICES,
        default="New Followup",
    )

    followup_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_response_followups",
    )

    comment = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    # ==========================================
    # SAVE
    # ==========================================

    def save(self, *args, **kwargs):

        # Generate Followup Number
        if not self.followup_no:

            with transaction.atomic():

                last = (
                    Followup.objects
                    .select_for_update()
                    .order_by("-followup_no")
                    .first()
                )

                if last and last.followup_no:
                    number = int(last.followup_no[2:]) + 1
                else:
                    number = 1

                self.followup_no = f"RF{number:06d}"

        super().save(*args, **kwargs)

        # Refresh Response Status
        self.response.refresh_status()

        # Deal Done
        if self.status == "Deal Done":

            Response.objects.filter(pk=self.response_id).update(
                status="Deal_close",
                is_converted=True,
                converted_at=timezone.now(),
            )

    # ==========================================
    # DELETE
    # ==========================================

    def delete(self, *args, **kwargs):

        response = self.response

        super().delete(*args, **kwargs)

        response.refresh_status()

    # ==========================================
    # STRING
    # ==========================================

    def __str__(self):
        return f"{self.followup_no} - {self.status}"

    # ==========================================
    # META
    # ==========================================

    class Meta:
        ordering = ("-followup_date",)
        verbose_name = "Follow Up"
        verbose_name_plural = "2. Follow Ups"

        indexes = [
            models.Index(fields=["followup_no"]),
            models.Index(fields=["followup_date"]),
            models.Index(fields=["status"]),
        ]

# =======================
#  Comment
# =======================
class Comment(BaseModel):
    response = models.ForeignKey(
        Response,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    comment = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Comment {self.id} - {self.comment[:25] if self.comment else ''}"


# =======================
#  Voice Recording
# =======================
class VoiceRecording(BaseModel):
    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name='recordings'
    )

    file = models.FileField(upload_to='voice_recordings/')
    note = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return f"Recording {self.id} - {self.file.name}"
