from django.db import models

from apps.core.models import BaseModel
from apps.utility.models import Location, PostalCode


# ==========================================================
# MASTER TABLES
# ==========================================================

class CompanyIndustry(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Company Industry"
        verbose_name_plural = "Company Industries"

    def __str__(self):
        return self.name


class CompanyType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Company Type"
        verbose_name_plural = "Company Types"

    def __str__(self):
        return self.name


class CompanySize(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Company Size"
        verbose_name_plural = "Company Sizes"

    def __str__(self):
        return self.name


# ==========================================================
# COMPANY
# ==========================================================

class Company(BaseModel):

    name = models.CharField(max_length=200)

    legal_name = models.CharField(
        max_length=250,
        blank=True,
    )

    industry = models.ForeignKey(
        CompanyIndustry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    company_type = models.ForeignKey(
        CompanyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    company_size = models.ForeignKey(
        CompanySize,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    logo = models.ImageField(
        upload_to="companies/logo/",
        blank=True,
        null=True,
    )

    website = models.URLField(blank=True)

    email = models.EmailField(blank=True)

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    alternate_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    gst_number = models.CharField(
        max_length=20,
        blank=True,
    )

    pan_number = models.CharField(
        max_length=20,
        blank=True,
    )

    cin_number = models.CharField(
        max_length=30,
        blank=True,
    )

    founded_year = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    employee_strength = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    address = models.TextField(blank=True)

    about = models.TextField(blank=True)

    facebook = models.URLField(blank=True)

    instagram = models.URLField(blank=True)

    linkedin = models.URLField(blank=True)

    twitter = models.URLField(blank=True)

    youtube = models.URLField(blank=True)

    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
# BRANCH
# ==========================================================

class Branch(BaseModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="branches",
    )

    name = models.CharField(max_length=200)

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(blank=True)

    manager_name = models.CharField(
        max_length=150,
        blank=True,
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    address = models.TextField(blank=True)

    class Meta:
        unique_together = ("company", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.company} - {self.name}"


# ==========================================================
# DEPARTMENT
# ==========================================================

class Department(BaseModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="departments",
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("company", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
# DESIGNATION
# ==========================================================

class Designation(BaseModel):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="designations",
    )

    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ("department", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
# COMPANY CONTACT
# ==========================================================

class CompanyContact(BaseModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="contacts",
    )

    name = models.CharField(max_length=150)

    designation = models.CharField(
        max_length=150,
        blank=True,
    )

    email = models.EmailField(blank=True)

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
    )

    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
# COMPANY DOCUMENT
# ==========================================================

class CompanyDocument(BaseModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    title = models.CharField(max_length=200)

    file = models.FileField(
        upload_to="companies/documents/"
    )

    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title