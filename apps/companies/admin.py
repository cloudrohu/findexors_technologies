from django.contrib import admin
from django.utils.html import format_html
from apps.job.models import Job
from .models import (
    Company,
    CompanyStatus,
    CompanyCategory,
    CompanyIndustry,
    CompanyType,
    CompanySize,
    GoogleMapStatus,
    DocumentType,
    Branch,
    Department,
    Designation,
    CompanyContact,
    CompanyDocument,
    CompanyGallery,
)


# ==========================================================
# COMPANY STATUS
# ==========================================================

@admin.register(CompanyStatus)
class CompanyStatusAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "color",
        "icon",
        "sort_order",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "color",
    )

    ordering = (
        "sort_order",
        "name",
    )


# ==========================================================
# COMPANY CATEGORY
# ==========================================================

@admin.register(CompanyCategory)
class CompanyCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ==========================================================
# COMPANY INDUSTRY
# ==========================================================

@admin.register(CompanyIndustry)
class CompanyIndustryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ==========================================================
# COMPANY TYPE
# ==========================================================

@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ==========================================================
# COMPANY SIZE
# ==========================================================

@admin.register(CompanySize)
class CompanySizeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "min_employee",
        "max_employee",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "min_employee",
        "name",
    )


# ==========================================================
# GOOGLE MAP STATUS
# ==========================================================

@admin.register(GoogleMapStatus)
class GoogleMapStatusAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ==========================================================
# DOCUMENT TYPE
# ==========================================================

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
    )

    search_fields = (
        "name",
        "description",
    )


# ==========================================================
# COMPANY BRANCH INLINE
# ==========================================================

class BranchInline(admin.TabularInline):

    model = Branch

    extra = 0

    fields = (
        "name",
        "branch_code",
        "manager_name",
        "phone",
        "email",
        "city",
        "locality",
        "area",
        "postal_code",
        "is_head_office",
    )


# ==========================================================
# COMPANY DEPARTMENT INLINE
# ==========================================================

class DepartmentInline(admin.TabularInline):

    model = Department

    extra = 0

    fields = (
        "name",
        "description",
    )


# ==========================================================
# COMPANY CONTACT INLINE
# ==========================================================

class CompanyContactInline(admin.TabularInline):

    model = CompanyContact

    extra = 0

    fields = (
        "name",
        "designation",
        "email",
        "phone",
        "whatsapp",
        "is_primary",
        "notes",
    )


# ==========================================================
# COMPANY DOCUMENT INLINE
# ==========================================================

class CompanyDocumentInline(admin.TabularInline):

    model = CompanyDocument

    extra = 0

    fields = (
        "document_type",
        "title",
        "file",
        "issue_date",
        "expiry_date",
        "remarks",
    )


# ==========================================================
# COMPANY GALLERY INLINE
# ==========================================================

class CompanyGalleryInline(admin.TabularInline):

    model = CompanyGallery

    extra = 0

    fields = (
        "image",
        "image_preview",
        "title",
        "sort_order",
    )

    readonly_fields = (
        "image_preview",
    )

    @admin.display(description="Preview")
    def image_preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" width="80" height="60" '
                'style="object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )

        return "-"


# ==========================================================
# COMPANY JOB INLINE
# ==========================================================

class JobInline(admin.TabularInline):

    model = Job

    extra = 0

    show_change_link = True

    fields = (
        "title",
        "category",
        "industry",
        "location",
        "postal_code",
        "vacancy",
        "job_type",
        "work_mode",
        "status",
        "featured",
        "published",
        "expiry_date",
    )

    autocomplete_fields = (
        "title",
        "category",
        "industry",
        "location",
        "postal_code",
    )
# ==========================================================
# COMPANY ADMIN
# ==========================================================

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    # ======================================================
    # LIST DISPLAY
    # ======================================================

    list_display = (
        "id",
        "company_logo",
        "name",
        "category",
        "industry",
        "company_type",
        "city",
        "primary_phone",
        "rating_badge",
        "reviews_count",
        "status_badge",
        "featured_badge",
        "verified_badge",
    )

    # ======================================================
    # LIST FILTER
    # ======================================================

    list_filter = (
        "status",
        "category",
        "industry",
        "company_type",
        "company_size",
        "city",
        "google_business_status",
        "is_verified",
        "is_featured",
    )

    # ======================================================
    # SEARCH
    # ======================================================

    search_fields = (
        "id",
        "name",
        "legal_name",
        "slug",
        "primary_phone",
        "alternate_phone",
        "whatsapp",
        "email",
        "website",
        "gst_number",
        "pan_number",
        "cin_number",
    )

    # ======================================================
    # ORDERING
    # ======================================================

    ordering = (
        "name",
    )

    # ======================================================
    # PAGINATION
    # ======================================================

    list_per_page = 25

    # ======================================================
    # SELECT RELATED
    # ======================================================

    list_select_related = (
        "status",
        "assigned_to",
        "category",
        "industry",
        "company_type",
        "company_size",
        "city",
        "locality",
        "area",
        "postal_code",
        "google_business_status",
    )

    # ======================================================
    # READONLY
    # ======================================================

    readonly_fields = (
        "id",
        "company_logo_large",
        "cover_preview",
    )

    # ======================================================
    # INLINES
    # ======================================================

    inlines = (
        BranchInline,
        DepartmentInline,
        CompanyContactInline,
        CompanyDocumentInline,
        CompanyGalleryInline,
        JobInline,

    )

    # ======================================================
    # FIELDSETS
    # ======================================================

    fieldsets = (

        # --------------------------------------------------
        # SYSTEM
        # --------------------------------------------------

        (
            "System Information",
            {
                "fields": (
                    "id",
                    "status",
                    "assigned_to",
                )
            },
        ),

        # --------------------------------------------------
        # BASIC
        # --------------------------------------------------

        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "legal_name",
                    "slug",
                    "category",
                )
            },
        ),

        # --------------------------------------------------
        # CLASSIFICATION
        # --------------------------------------------------

        (
            "Classification",
            {
                "fields": (
                    "industry",
                    "company_type",
                    "company_size",
                )
            },
        ),

        # --------------------------------------------------
        # BRANDING
        # --------------------------------------------------

        (
            "Branding",
            {
                "fields": (
                    "logo",
                    "company_logo_large",
                    "cover_image",
                    "cover_preview",
                )
            },
        ),

        # --------------------------------------------------
        # CONTACT
        # --------------------------------------------------

        (
            "Contact Information",
            {
                "fields": (
                    "primary_phone",
                    "alternate_phone",
                    "whatsapp",
                    "email",
                    "website",
                )
            },
        ),

        # --------------------------------------------------
        # LOCATION
        # --------------------------------------------------

        (
            "Location",
            {
                "fields": (
                    "city",
                    "locality",
                    "area",
                    "postal_code",
                    "address",
                    "google_map",
                )
            },
        ),

        # --------------------------------------------------
        # BUSINESS
        # --------------------------------------------------

        (
            "Business Information",
            {
                "fields": (
                    "founded_year",
                    "employee_strength",
                    "gst_number",
                    "pan_number",
                    "cin_number",
                    "rating",
                    "reviews_count",
                    "google_business_status",
                )
            },
        ),

        # --------------------------------------------------
        # DESCRIPTION
        # --------------------------------------------------

        (
            "Description",
            {
                "fields": (
                    "short_description",
                    "about",
                )
            },
        ),

        # --------------------------------------------------
        # SOCIAL
        # --------------------------------------------------

        (
            "Social Media",
            {
                "fields": (
                    "facebook",
                    "instagram",
                    "linkedin",
                    "twitter",
                    "youtube",
                )
            },
        ),

        # --------------------------------------------------
        # SEO
        # --------------------------------------------------

        (
            "SEO",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                    "meta_keywords",
                )
            },
        ),

        # --------------------------------------------------
        # FLAGS
        # --------------------------------------------------

        (
            "Visibility & Flags",
            {
                "fields": (
                    "is_verified",
                    "is_featured",
                )
            },
        ),
    )

    # ======================================================
    # LOGO - LIST
    # ======================================================

    @admin.display(description="Logo")
    def company_logo(self, obj):

        if obj.logo:

            return format_html(
                '<img src="{}" width="45" height="45" '
                'style="object-fit:cover;border-radius:6px;" />',
                obj.logo.url,
            )

        return "-"

    # ======================================================
    # LOGO - DETAIL
    # ======================================================

    @admin.display(description="Logo Preview")
    def company_logo_large(self, obj):

        if obj.logo:

            return format_html(
                '<img src="{}" width="180" height="120" '
                'style="object-fit:cover;border-radius:8px;" />',
                obj.logo.url,
            )

        return "No logo uploaded"

    # ======================================================
    # COVER PREVIEW
    # ======================================================

    @admin.display(description="Cover Preview")
    def cover_preview(self, obj):

        if obj.cover_image:

            return format_html(
                '<img src="{}" width="300" height="150" '
                'style="object-fit:cover;border-radius:8px;" />',
                obj.cover_image.url,
            )

        return "No cover image uploaded"

    # ======================================================
    # RATING BADGE
    # ======================================================

    @admin.display(description="Rating")
    def rating_badge(self, obj):

        if obj.rating is not None:

            rating = f"{float(obj.rating):.1f}"

            return format_html(
                '<strong>{} ⭐</strong>',
                rating,
            )

        return "-"

    # ======================================================
    # STATUS BADGE
    # ======================================================

    @admin.display(description="Status")
    def status_badge(self, obj):

        if not obj.status:

            return "-"

        return format_html(
            '<span style="padding:4px 8px;'
            'border-radius:12px;'
            'background:#eef2ff;'
            'color:#3730a3;'
            'font-weight:600;">{}</span>',
            obj.status.name,
        )

    # ======================================================
    # VERIFIED BADGE
    # ======================================================

    @admin.display(description="Verified")
    def verified_badge(self, obj):

        if obj.is_verified:

            return format_html(
                '<span style="padding:4px 8px;'
                'border-radius:12px;'
                'background:#dcfce7;'
                'color:#166534;'
                'font-weight:600;">{}</span>',
                "✓ Verified",
            )

        return format_html(
            '<span style="color:#999;">{}</span>',
            "—",
        )

    # ======================================================
    # FEATURED BADGE
    # ======================================================

    @admin.display(description="Featured")
    def featured_badge(self, obj):

        if obj.is_featured:

            return format_html(
                '<span style="padding:4px 8px;'
                'border-radius:12px;'
                'background:#fef3c7;'
                'color:#92400e;'
                'font-weight:600;">{}</span>',
                "★ Featured",
            )

        return format_html(
            '<span style="color:#999;">{}</span>',
            "—",
        )


# ==========================================================
# BRANCH ADMIN
# ==========================================================

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "company",
        "branch_code",
        "manager_name",
        "city",
        "is_head_office",
    )

    list_filter = (
        "is_head_office",
        "city",
    )

    search_fields = (
        "name",
        "branch_code",
        "manager_name",
        "phone",
        "email",
        "company__name",
    )

    list_select_related = (
        "company",
        "city",
        "locality",
        "area",
        "postal_code",
    )


# ==========================================================
# DEPARTMENT ADMIN
# ==========================================================

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "company",
        "description",
    )

    search_fields = (
        "name",
        "company__name",
    )

    list_select_related = (
        "company",
    )


# ==========================================================
# DESIGNATION ADMIN
# ==========================================================

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "department",
    )

    search_fields = (
        "name",
        "department__name",
        "department__company__name",
    )

    list_select_related = (
        "department",
        "department__company",
    )


# ==========================================================
# COMPANY CONTACT ADMIN
# ==========================================================

@admin.register(CompanyContact)
class CompanyContactAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "company",
        "designation",
        "email",
        "phone",
        "is_primary",
    )

    list_filter = (
        "is_primary",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "whatsapp",
        "company__name",
    )

    list_select_related = (
        "company",
        "designation",
    )


# ==========================================================
# COMPANY DOCUMENT ADMIN
# ==========================================================

@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company",
        "document_type",
        "issue_date",
        "expiry_date",
    )

    list_filter = (
        "document_type",
        "issue_date",
        "expiry_date",
    )

    search_fields = (
        "title",
        "remarks",
        "company__name",
    )

    list_select_related = (
        "company",
        "document_type",
    )


# ==========================================================
# COMPANY GALLERY ADMIN
# ==========================================================

@admin.register(CompanyGallery)
class CompanyGalleryAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "company",
        "title",
        "sort_order",
    )

    list_filter = (
        "company",
    )

    search_fields = (
        "title",
        "company__name",
    )

    ordering = (
        "company",
        "sort_order",
    )

    list_select_related = (
        "company",
    )

    readonly_fields = (
        "image_preview",
    )

    fields = (
        "company",
        "image",
        "image_preview",
        "title",
        "sort_order",
    )

    @admin.display(description="Preview")
    def image_preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" width="100" height="70" '
                'style="object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )

        return "-"