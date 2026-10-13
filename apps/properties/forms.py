from django import forms

from .models import (
    Developer,
    Architects,
    Engineer,
    Project,
    Meeting,
)


# ============================================================
# COMMON FORM CSS
# ============================================================

TEXT_INPUT_CLASS = "form-control"
SELECT_CLASS = "form-select"
TEXTAREA_CLASS = "form-control"
CHECKBOX_CLASS = "form-check-input"


# ============================================================
# DEVELOPER FORM
# ============================================================

class DeveloperEditForm(forms.ModelForm):

    class Meta:
        model = Developer

        fields = [
            "title",
            "city",
            "locality",
            "area",
            "postal_code",
            "address",
            "contact_person",
            "contact_no",
            "email",
            "google_map",
            "web_site",
            "keywords",
            "about_developer",
            "note",
            "logo",
            "featured_builder",
            "is_verified",
            "is_featured",
            "calling_status",
            "assigned_to",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Developer Name",
                }
            ),

            "city": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "locality": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "area": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "postal_code": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 3,
                    "placeholder": "Complete Address",
                }
            ),

            "contact_person": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Contact Person",
                }
            ),

            "contact_no": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Contact Number",
                    "maxlength": "10",
                    "inputmode": "numeric",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Email Address",
                }
            ),

            "google_map": forms.URLInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Google Maps URL",
                }
            ),

            "web_site": forms.URLInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Website URL",
                }
            ),

            "keywords": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Keywords",
                }
            ),

            "about_developer": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 6,
                    "placeholder": "About Developer",
                }
            ),

            "note": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 4,
                    "placeholder": "Internal Notes",
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                }
            ),

            "featured_builder": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "is_verified": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "is_featured": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "calling_status": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),
        }

    def clean_contact_no(self):
        contact_no = self.cleaned_data.get("contact_no")

        if contact_no:
            digits = "".join(
                character
                for character in str(contact_no)
                if character.isdigit()
            )

            if len(digits) < 10:
                raise forms.ValidationError(
                    "Please enter a valid 10 digit contact number."
                )

            return digits[-10:]

        return contact_no


# ============================================================
# ARCHITECT FORM
# ============================================================

class ArchitectEditForm(forms.ModelForm):

    class Meta:
        model = Architects

        fields = [
            "title",
            "city",
            "locality",
            "area",
            "postal_code",
            "address",
            "contact_person",
            "contact_no",
            "email",
            "google_map",
            "web_site",
            "keywords",
            "about_architect",
            "note",
            "logo",
            "featured_architect",
            "is_verified",
            "is_featured",
            "calling_status",
            "assigned_to",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Architect Name",
                }
            ),

            "city": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "locality": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "area": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "postal_code": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 3,
                    "placeholder": "Complete Address",
                }
            ),

            "contact_person": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Contact Person",
                }
            ),

            "contact_no": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Contact Number",
                    "maxlength": "10",
                    "inputmode": "numeric",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Email Address",
                }
            ),

            "google_map": forms.URLInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Google Maps URL",
                }
            ),

            "web_site": forms.URLInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Website URL",
                }
            ),

            "keywords": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Keywords",
                }
            ),

            "about_architect": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 6,
                    "placeholder": "About Architect",
                }
            ),

            "note": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 4,
                    "placeholder": "Internal Notes",
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                }
            ),

            "featured_architect": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "is_verified": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "is_featured": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "calling_status": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),
        }

    def clean_contact_no(self):
        contact_no = self.cleaned_data.get("contact_no")

        if contact_no:
            digits = "".join(
                character
                for character in str(contact_no)
                if character.isdigit()
            )

            if len(digits) < 10:
                raise forms.ValidationError(
                    "Please enter a valid 10 digit contact number."
                )

            return digits[-10:]

        return contact_no


# ============================================================
# ENGINEER FORM
# ============================================================

class EngineerEditForm(forms.ModelForm):

    class Meta:
        model = Engineer

        fields = [
            "title",
            "city",
            "locality",
            "area",
            "postal_code",
            "address",
            "contact_person",
            "contact_no",
            "email",
            "google_map",
            "web_site",
            "keywords",
            "about_engineer",
            "note",
            "logo",
            "featured_engineer",
            "is_verified",
            "is_featured",
            "calling_status",
            "assigned_to",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Engineer Name",
                }
            ),

            "city": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "locality": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "area": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "postal_code": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 3,
                    "placeholder": "Complete Address",
                }
            ),

            "contact_person": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Contact Person",
                }
            ),

            "contact_no": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Contact Number",
                    "maxlength": "10",
                    "inputmode": "numeric",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Email Address",
                }
            ),

            "google_map": forms.URLInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Google Maps URL",
                }
            ),

            "web_site": forms.URLInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Website URL",
                }
            ),

            "keywords": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Keywords",
                }
            ),

            "about_engineer": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 6,
                    "placeholder": "About Engineer",
                }
            ),

            "note": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 4,
                    "placeholder": "Internal Notes",
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                }
            ),

            "featured_engineer": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "is_verified": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "is_featured": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "calling_status": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),
        }

    def clean_contact_no(self):
        contact_no = self.cleaned_data.get("contact_no")

        if contact_no:
            digits = "".join(
                character
                for character in str(contact_no)
                if character.isdigit()
            )

            if len(digits) < 10:
                raise forms.ValidationError(
                    "Please enter a valid 10 digit contact number."
                )

            return digits[-10:]

        return contact_no


# ============================================================
# PROJECT FORM
# ============================================================

class ProjectEditForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            # Status / certificates
            "calling_status",
            "occupancy_certificate",
            "commencement_certificate",
            "construction_status",

            # Core
            "property_type",
            "parent",
            "project_name",

            # Relations
            "developer",
            "architect",
            "engineer",

            # Location
            "city",
            "locality",
            "area",
            "postal_code",
            "address",

            # Property information
            "land_parcel",
            "bhk_type",
            "floor",
            "possession_year",
            "possession_month",
            "luxurious",
            "pricing",

            # Media / marketing
            "youtube_embed_id",
            "featured_property",
            "balcony",
            "image",
            "google_map_iframe",
        ]

        widgets = {

            "calling_status": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "occupancy_certificate": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "commencement_certificate": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "construction_status": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "property_type": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "parent": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "project_name": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Project Name",
                }
            ),

            "developer": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "architect": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "engineer": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "city": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "locality": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "area": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "postal_code": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 3,
                    "placeholder": "Project Address",
                }
            ),

            "land_parcel": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Land Parcel",
                }
            ),

            "bhk_type": forms.SelectMultiple(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "floor": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Floor",
                }
            ),

            "possession_year": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "possession_month": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "luxurious": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Luxury / Lifestyle Details",
                }
            ),

            "pricing": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Pricing",
                }
            ),

            "youtube_embed_id": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "YouTube Video ID",
                }
            ),

            "featured_property": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "balcony": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASS,
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                }
            ),

            "google_map_iframe": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 5,
                    "placeholder": "Google Map Iframe",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Current project ko khud ka parent banne se rokna
        if self.instance and self.instance.pk:

            self.fields["parent"].queryset = (
                Project.objects
                .exclude(pk=self.instance.pk)
                .order_by("project_name")
            )

        # Better ordering
        self.fields["developer"].queryset = (
            Developer.objects.order_by("title")
        )

        self.fields["architect"].queryset = (
            Architects.objects.order_by("title")
        )

        self.fields["engineer"].queryset = (
            Engineer.objects.order_by("title")
        )


# ============================================================
# MEETING FORM
# ============================================================

class MeetingEditForm(forms.ModelForm):

    class Meta:
        model = Meeting

        fields = [
            "status",
            "meeting_date",
            "assigned_to",
            "comment",
        ]

        widgets = {

            "status": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "meeting_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "type": "datetime-local",
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 6,
                    "placeholder": "Meeting Comment",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["meeting_date"].input_formats = [
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d %H:%M",
        ]