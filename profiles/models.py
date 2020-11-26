from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import  slugify
from django.db.models import Q

from .utils import get_random_code


class ProfileManager(models.Manager):
    # here i use 'sender'---> and sender is actually 'me' or requested user
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        relationships = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print('relationships are here: ', relationships)

        # the difference between 'accepted = [] and accepted = set([])' is that if you are going to 
        # add just [] --> you need to use 'append' but for 'set([])' you need to use 'add' instead
        # and because here it's show us duplicate user--> so we have to elemintate that a profile 
        # should exists one time either 'sender' or 'receiver'---> that's why i used 'set([])' here
        accepted = set([])
        for rel in relationships:
            if rel.status == 'accepted':
                # we wanna added those who are accepted to prevent showing in our invite list anymore
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print("accepted here: ", accepted)
        

        # if not in our accepted list so we should listed on available
        available = [profile for profile in profiles if profile not in accepted]
        print("available profiles are here: ", available)
        return available
        
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

class Profile(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name  = models.CharField(max_length=50, blank=True)
    email      = models.EmailField(blank=True, max_length=100)
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    bio        = models.TextField(max_length=300, default='No bio define')
    country    = models.CharField(max_length=100, blank=True)
    avatar     = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends    = models.ManyToManyField(User, blank=True, related_name='friends')
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)
    slug       = models.SlugField(unique=True, blank=True)

    objects = ProfileManager()

    def get_friends(self):
        return self.friends.all()

    def get_friend_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        # because here we set related_name 'posts' in author. otherwise we
        # need to do like ---> self.post_set.all().count()
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0 
        for like in likes:
            if like.value=='Like':
                total_liked += 1 
        return total_liked

    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for post in posts:
            total_liked += post.liked.all().count()
        return total_liked
        
    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"
    
    def save(self, *args, **kwargs):
        # check if it's exists
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name)+" "+str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug+" "+str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug)
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    # instead of doing Relationship.objects.received(myprofile)--> i gonna use manager like follows:
    def invitation_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs 

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RelationshipManager()
    
    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'