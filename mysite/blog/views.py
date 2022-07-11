from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post,Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,DetailView,
                                  CreateView, UpdateView, DeleteView)

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

# Bascially a SQL query on your Model. Grab the Post Model, all of the objects there,
# and filter based on the following conditions.
# FIELD LOOKUPS IN THE DJANGO DOCUMENTATION - LIKE 'WHERE' IN SQL
# Field Conditions: __lte = less than or equal to
# order_by('-published_date')) means order the posts in descending order
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
# LoginRequiredMixin is the CBV version of a decorator (@)
# BELOW ARE CALLED ATTRIBUTES
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post # Connected to the model we will be deleting from
    success_url = reverse_lazy('post_list') # Waits until you have actually deleted it to give you back the success_url

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

# For the list of Drafts, make sure there is no publication date
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


################################################################################
################################################################################
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)




@login_required
def add_comment_to_post(request,pk): # Take in request and pk, linking the comment to the post
    post = get_object_or_404(Post,pk=pk) # Get the post object, or the 404 page. Pass in the Post model and pk=pk
    if request.method == 'POST': # If someone has filled in the form and hit enter
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post # The comment.post, make it equal to the post itself
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve() # approve method inside of models.py
    return redirect('post_detail',pk=comment.post.pk) # See Comment Model - the comment is connected to a particular post. After approving comment, to go to the post, you need the post.pk. Which goes to the Post model to get the pk.

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk # Save as a separate variable, so when you delete it, you can still grab it on the last line below pk=post_pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
