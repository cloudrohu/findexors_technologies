# apps/properties/resources.py

from import_export import resources
from .models import Developer


class DeveloperResource(resources.ModelResource):

    class Meta:
        model = Developer

        exclude = (
            "created_by",
            "updated_by",
        )

        import_id_fields = ("slug",)
        skip_unchanged = True
        report_skipped = True