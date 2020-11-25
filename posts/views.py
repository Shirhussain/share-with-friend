from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView
from django.urls import  reverse_lazy
from django.contrib import messages

from .models import Post, Comment, Like
from profiles.models import Profile
from .forms import PostForm, CommentForm


def post_comment_create_list_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    # initials---> if we don't use this two line of code like this so we have conflict 
    # when a user wanna create a post and comment---> which give as error 
    # it assume that at the same time you must provide post and comment in one click.
    p_form = PostForm()
    c_form = CommentForm()
    # instead of mesages we can use this line of code. 
    post_added = False 
    
    if 'submit_p_form' in request.POST:
        p_form = PostForm(request.POST or None, request.FILES or None)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            # then reset the form
            p_form = PostForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentForm(request.POST or None)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.author = profile
            # this 'post_id' is come form c_form  when submitted which is a hidden input
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentForm()

    context = {
        'posts': posts,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added
    }
    
    return render(request, 'posts/main.html', context)


def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        # if already person liked the post
        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value =='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post.save()
            like.save()
    return redirect('posts:post_comment_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    # we use 'reverse' for function base view and 'reverse_lazy' for class base view
    success_url = reverse_lazy('posts:post_comment_list')

    def get_object(self, *args, **kwargs):
        # for deleting specific post we need the 'pk'
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        if not post.author.user == self.request.user:
            messages.warning(self.request, "You need to be an author or the post in order to delete a post")
        return post 
    

class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:post_comment_list')

    # the above lines of code is working but for making sure that our user is owner or authenticated user 
    # then then we should update.
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "you need to be an author of the post in order to updated it")
            return super().form_invalid(form)


