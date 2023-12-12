from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Announcement
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, AnnouncementForm, UpdateAnnouncementForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotAllowed, HttpResponse

@login_required
def get_user_announcement_list(request):
    user_announcements = Announcement.objects.filter(user_profile=request.user)
    return render(request, 'announcement/list_of_user_announcements.html', {'announcements': user_announcements})


def get_public_announcements(request):
    # Фільтруємо анонси за полем access
    announcements = Announcement.objects.filter(access='public')
    return render(request, 'announcement/list_of_public_announcements.html', {'announcements': announcements})

@login_required
def get_local_announcements(request):
    location = request.user.location
    print(location)
    # Fetch local announcements for the user's location
    announcements = Announcement.objects.filter(access='local', location__iexact=location)

    return render(request, 'announcement/list_of_local_announcements.html', {'announcements': announcements, 'location': location})
  

@csrf_exempt
def get_announcement_by_id(request, id):
    announcement = Announcement.objects.get(id=id)

    # Перевіряємо доступ до анонсу
    if announcement.access == 'public' or (request.user.is_authenticated and request.user.location == announcement.location):
        return render(request, 'announcement/announcement.html', {'announcement': announcement})
    else:
        return render(request, '404.html')

@csrf_exempt
@login_required(login_url='login')  # Add this decorator to ensure the user is logged in
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            # Check if the user is authenticated
            if request.user.is_authenticated:
                user_location = request.user.location
            else:
                user_location = None

            # Creating an announcement
            announcement = form.save(commit=False)
            announcement.location = user_location
            announcement.user_profile = request.user 
            announcement.save()

            return redirect('home')  # Replace 'home' with the desired redirect URL after successful form submission
    else:
        form = AnnouncementForm()

    return render(request, 'announcement/create_announcement.html', {'form': form})


@login_required
def update_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id, user_profile=request.user)

    if request.method == 'POST':
        form = UpdateAnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('/announcements/user')
    else:
        form = UpdateAnnouncementForm(instance=announcement)

    return render(request, 'announcement/update_announcement.html', {'form': form, 'announcement': announcement})
    
# @login_required 
# def delete_announcement(request, id):
#     announcement = get_object_or_404(Announcement, id=id)
#     announcement.delete()
#     return redirect('/announcements/user')


@login_required
@require_http_methods(["DELETE"])
def delete_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)

    if request.method == 'DELETE':
        announcement.delete()
        return HttpResponse(status=204)  # Successful DELETE request, no content
    else:
        return HttpResponseNotAllowed(['DELETE'])

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login')  # Замініть 'home' на ваш шлях при необхідності
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Замініть 'home' на ваш шлях при необхідності
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def user_logout(request):
    logout(request)
    return redirect('home')  # Замініть 'home' на шлях, куди ви хочете перенаправити після виходу
