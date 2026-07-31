from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ==========================================
    # Admin AJAX APIs
    # ==========================================


    # ==========================================
    # Grappelli
    # ==========================================
    path(
        "grappelli/",
        include("grappelli.urls"),
    ),

    # ==========================================
    # Django Admin
    # ==========================================
    path(
        "admin/",
        admin.site.urls,
    ),


    path("admin/ajax/", include("apps.utility.admin.urls")),
    # ==========================================
    # Dashboard
    # ==========================================
    path(
        "",
        include("apps.dashboard.urls"),
    ),

    # ==========================================
    # Jobs
    # ==========================================
    path(
        "jobs/",
        include("apps.job.urls"),
    ),

    # ==========================================
    # Companies
    # ==========================================
    path(
        "companies/",
        include("apps.companies.urls"),
    ),

    # ==========================================
    # CKEditor
    # ==========================================
    path(
        "ckeditor/",
        include("ckeditor_uploader.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )