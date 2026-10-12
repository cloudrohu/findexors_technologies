from django.urls import path
from . import views


app_name = "meetings"


urlpatterns = [

    path(
        "property/",
        views.property_meetings,
        name="property_meetings"
    ),

]