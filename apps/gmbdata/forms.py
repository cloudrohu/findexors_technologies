from django import forms

from .models import (
    Realty,
    Interior,
    Refrense,
    Meeting,
    Followup,
    Comment,
    VoiceRecording,
    Visit,
)


# =========================================================
# REALTY FORM
# =========================================================

class RealtyForm(forms.ModelForm):

    class Meta:
        model = Realty

        fields = [
            "name",
            "name_for_emails",

            # Location
            "city",
            "locality",
            "area",
            "postal_code",
            "address",

            # Google
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

            # Status
            "status",
            "assigned_to",

            # Verification
            "is_verified",
            "is_featured",

            # Slug
            "slug",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company Name",
                }
            ),

            "name_for_emails": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Name for Emails",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Website",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Address",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "about": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "working_hours": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "city": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "locality": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "area": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "postal_code": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "category_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "type": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "street": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "city_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "postal_code_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "latitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "any",
                }
            ),

            "longitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "any",
                }
            ),

            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.1",
                }
            ),

            "reviews": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "place_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "google_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "cid": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "business_status": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "logo": forms.URLInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


# =========================================================
# INTERIOR FORM
# =========================================================

class InteriorForm(forms.ModelForm):

    class Meta:
        model = Interior

        fields = "__all__"

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Interior Company Name",
                }
            ),

            "name_for_emails": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Name for Emails",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "10 Digit Phone Number",
                    "maxlength": "20",
                }
            ),

            "other_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Other Phone Number",
                    "maxlength": "20",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Address",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Description",
                }
            ),

            "about": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "About",
                }
            ),

            "working_hours": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Working Hours",
                }
            ),

            "google_map": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Google Map",
                }
            ),

            "category_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "type": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "street": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "city_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "postal_code_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "latitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.0000001",
                }
            ),

            "longitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.0000001",
                }
            ),

            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.1",
                    "min": "0",
                    "max": "5",
                }
            ),

            "reviews": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "place_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "google_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "cid": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "business_status": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    # =====================================================
    # PHONE CLEAN
    # =====================================================

    def clean_phone(self):

        phone = self.cleaned_data.get("phone")

        if phone:
            digits = "".join(
                char for char in str(phone)
                if char.isdigit()
            )

            if len(digits) >= 10:
                return digits[-10:]

            return digits

        return phone

    # =====================================================
    # OTHER PHONE CLEAN
    # =====================================================

    def clean_other_phone(self):

        phone = self.cleaned_data.get("other_phone")

        if phone:
            digits = "".join(
                char for char in str(phone)
                if char.isdigit()
            )

            if len(digits) >= 10:
                return digits[-10:]

            return digits

        return phone

# =========================================================
# REFRENSE FORM
# =========================================================

class RefrenseForm(forms.ModelForm):

    class Meta:
        model = Refrense

        fields = [
            "refrense_name",

            # Location
            "city",
            "locality",
            "area",
            "address",

            # Contact
            "contact_no",
            "other_no",
            "email",
            "website",

            # Google
            "google_map",
            "rating",
            "reviews_count",
            "business_status_raw",

            # Status
            "status",
            "assigned_to",

            # Image
            "logo",

            # Verification
            "is_verified",
            "is_featured",

            # Slug
            "slug",
        ]

        widgets = {
            "refrense_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Reference Name",
                }
            ),

            "contact_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Contact Number",
                }
            ),

            "other_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Other Number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Website",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "google_map": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "city": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "locality": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "area": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.1",
                }
            ),

            "reviews_count": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "business_status_raw": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


# =========================================================
# MEETING FORM
# =========================================================

class MeetingForm(forms.ModelForm):

    class Meta:
        model = Meeting

        fields = [
            "realty",
            "meeting_no",
            "status",
            "meeting_date",
            "assigned_to",
            "comment",
        ]

        widgets = {
            "realty": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "meeting_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "meeting_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "comment": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Comment",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Meeting number automatically generated by model
        self.fields["meeting_no"].required = False


# =========================================================
# FOLLOWUP FORM
# =========================================================

class FollowupForm(forms.ModelForm):

    class Meta:
        model = Followup

        fields = [
            "realty",
            "followup_no",
            "status",
            "followup_date",
            "assigned_to",
            "comment",
        ]

        widgets = {
            "realty": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "followup_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "followup_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "comment": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Comment",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["followup_no"].required = False


# =========================================================
# COMMENT FORM
# =========================================================

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = [
            "realty",
            "comment",
        ]

        widgets = {
            "realty": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write comment...",
                }
            ),
        }


# =========================================================
# VOICE RECORDING FORM
# =========================================================

class VoiceRecordingForm(forms.ModelForm):

    class Meta:
        model = VoiceRecording

        fields = [
            "realty",
            "file",
            "uploaded_by",
        ]

        widgets = {
            "realty": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "uploaded_by": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


# =========================================================
# VISIT FORM
# =========================================================

class VisitForm(forms.ModelForm):

    class Meta:
        model = Visit

        fields = [
            "realty",
            "visit_date",
            "status",
            "assigned_to",
            "comment",
        ]

        widgets = {
            "realty": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "visit_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

            "status": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Visit Status",
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Comment",
                }
            ),
        }