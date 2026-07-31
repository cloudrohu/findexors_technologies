from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Grappelli (Admin se pehle)
    path("grappelli/", include("grappelli.urls")),

    # Django Admin
    path("admin/", admin.site.urls),

    # Dashboard
    path("", include("apps.dashboard.urls")),

    # Recruitment / HRMS
    path("jobs/", include("apps.job.urls")),

    # Companies
    path("companies/", include("apps.companies.urls")),

    # Location
    #path("locations/", include("apps.utility.urls")),

    # CKEditor
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )