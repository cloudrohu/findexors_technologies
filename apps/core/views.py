from django.shortcuts import render

from apps.business.models import Business
from apps.business_utility.models import BusinessCategory


def home(request):

    # ==========================================
    # FEATURED CATEGORIES
    # ==========================================

    categories = (
        BusinessCategory.objects
        .filter(
            is_active=True,
            is_featured=True,
            parent__isnull=True,
        )
        .order_by(
            "display_order",
            "name",
        )[:6]
    )


    # ==========================================
    # FEATURED BUSINESSES
    # ==========================================

    featured_businesses = (
        Business.objects
        .filter(
            is_active=True,
            is_featured=True,
        )
        .select_related(
            "category",
            "location",
        )
        .order_by(
            "-is_premium",
            "-is_verified",
            "-rating",
            "-review_count",
            "-created_at",
        )[:8]
    )


    # ==========================================
    # STATISTICS
    # ==========================================

    business_count = (
        Business.objects
        .filter(is_active=True)
        .count()
    )

    category_count = (
        BusinessCategory.objects
        .filter(is_active=True)
        .count()
    )


    context = {
        "categories": categories,
        "featured_businesses": featured_businesses,
        "business_count": business_count,
        "category_count": category_count,
    }


    return render(
        request,
        "index.html",
        context,
    )