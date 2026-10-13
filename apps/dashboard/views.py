from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


# =========================================================
# DASHBOARD
# =========================================================

@login_required(login_url="dashboard_login")
def dashboard_index(request):

    return render(
        request,
        "dashboard/index.html"
    )


# =========================================================
# LOGIN
# =========================================================

def dashboard_login(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            if not user.is_active:
                messages.error(
                    request,
                    "Your account is inactive."
                )

                return redirect("dashboard_login")

            login(request, user)

            # Redirect to originally requested page
            next_url = request.POST.get("next") or request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "dashboard/login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required(login_url="dashboard_login")
def dashboard_logout(request):

    logout(request)

    return redirect("dashboard_login")