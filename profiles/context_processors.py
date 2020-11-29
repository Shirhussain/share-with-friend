from .models import Profile, Relationship

def profile_pic(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        pic = profile.avatar
        return {'picture': pic}
    return {}

def invitations_received_no(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = Relationship.objects.invitation_received(profile_obj).count()
        return {'invites_num': qs_count}
    return {}
    

