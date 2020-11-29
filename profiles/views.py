from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404

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
    # if you wanna know more about lambda have look to this blog
    # https://blog.pyplane.com/blog/map-filter-conditional-list-comprehension/
    # by default in our invitation queryset we have bot sender and receiver but we just need sender 
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results)== 0:
        is_empty = True

    context = {
        'qs': results, 
        'is_empty': is_empty
    }
    return render(request, 'profiles/my_invitation.html', context)


def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invitation')


def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invitation')    



def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs': qs 
    }
    return render(request, 'profiles/to_invite_profile_list.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     return profile


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context


# def profile_list_view(request):
#     user = request.user 
#     qs = Profile.objects.get_all_profiles(user)

#     context = {
#         'qs': qs 
#     }
#     return render(request, 'profiles/profile_list.html', context)


# i wanna refactore the above function in CBV
class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # for making sure that we are geting the requested user do the following lines of code 
        # cuz sometime i use just request.user and got errors
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        # relationship_receiver
        # and here when we are the sender of invite
        rel_r = Relationship.objects.filter(sender=profile)
        # rel_sender
        # we are the receiver of the invite
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        
        for item in rel_s:
            rel_sender.append(item.sender.user)
        # we can check that if the link of our queryset is = '0' then we gonna create another 
        # context dictionary like 'is_empty' and return it to True because by default it set to False
        context["rel_sender"] = rel_sender
        context["rel_receiver"] = rel_receiver
        context["is_empty"] = False 
        if len(self.get_queryset())==0:
            context["is_empty"] = True
        return context


def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user 
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        print("This is the relation: ", rel)
        # I wanna redirect to the same path so here is the way
        return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect('profiles:myprofile')


def remove_from_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user 
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        # it's somehow complected cuz we don't know who is the sender and who is the receiver 
        # it means that i don't know if i invited a particular user or vise versa 
        # here is the deal that you have to remove yourself from your friend list and vis versa 
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect('profiles:myprofile')
    