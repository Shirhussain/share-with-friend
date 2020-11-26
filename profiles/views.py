from django.shortcuts import render

from .models import Profile, Relationship
from .forms import ProfileForm

def my_profile_view(request):
    """Create profile for user"""
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None ,instance=profile)
    confirm = False 
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm
    }
    return render(request, "profiles/myprofile.html", context)


def invitation_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitation_received(profile)
    print("your initation list is",qs)
    context = {
        'qs': qs
    }
    return render(request, 'profiles/my_invitation.html', context)


def profile_list_view(request):
    user = request.user 
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs': qs 
    }
    return render(request, 'profiles/profile_list.html', context)

def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs': qs 
    }
    return render(request, 'profiles/to_invite_profile_list.html', context)