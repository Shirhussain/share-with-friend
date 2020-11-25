from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ('content', 'image')


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Add a comment ...'})    
    )
    class Meta:
        model = Comment
        fields = ('content',)