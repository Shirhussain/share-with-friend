from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import  slugify

from .utils import get_random_code


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

    def get_friends(self):
        return self.friends.all()

    def get_friend_no(self):
        return self.friends.all().count()
        
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

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'