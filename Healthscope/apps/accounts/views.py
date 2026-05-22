from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from datetime import date


# HOME
def home(request):
    users = User.objects.all()
    return render(request, 'accounts/accounts.html', {"users": users})


# LOGIN
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # ✅ IMPORTANT LOGIC
            if Profile.objects.filter(user=user).exists():
                return redirect('home')   # already filled → go profile
            else:
                return redirect('profile_form')  # first time → fill form

    return render(request, 'accounts/login.html')


# REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Username already exists"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "accounts/register.html")


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect("home")


# PROFILE CREATE
@login_required
def profile_create(request):

    # ✅ If already exists → don't allow again
    if Profile.objects.filter(user=request.user).exists():
        return redirect('profile')

    if request.method == "POST":
        profile = Profile(user=request.user)

        profile.name = request.POST.get('name')
        profile.age = request.POST.get('age')
        profile.gender = request.POST.get('gender')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        profile.blood_group = request.POST.get('blood_group')
        profile.comment = request.POST.get('comment')

        # DOB
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')

        if day and month and year:
            try:
                profile.dob = date(int(year), int(month), int(day))
            except:
                pass

        profile.save()
        return redirect('profile')

    return render(request, 'accounts/profile_form.html')


# PROFILE VIEW
@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('profile_form')

    return render(request, 'accounts/profile.html', {'profile': profile})


# PROFILE UPDATE
@login_required
def profile_update(request):
    user = request.user

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return redirect('profile_form')

    if request.method == "POST":

        # USER UPDATE
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        password = request.POST.get('password')
        if password:
            user.set_password(password)
            login(request, user)  # ✅ stay logged in after password change

        user.save()

        # PROFILE UPDATE
        profile.name = request.POST.get('name')
        profile.age = request.POST.get('age')
        profile.gender = request.POST.get('gender')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        profile.blood_group = request.POST.get('blood_group')
        profile.comment = request.POST.get('comment')

        # DOB
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')

        if day and month and year:
            profile.dob = date(int(year), int(month), int(day))

        profile.save()

        return redirect('profile')

    return render(request, 'accounts/update.html', {'profile': profile})