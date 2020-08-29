from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from .models import Blog, Comment, Like
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from .forms import CommentForm

# Create your views here.

class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'blog_app/myblogs.html'


class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'blog_app/blog_list.html'
    

class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog_app/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace('\' ', '-')
        blog_obj.slug = title.replace(' ', '-') + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))

@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Like.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else: liked = False
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('blog_app:blog_details', kwargs={'slug': slug}))

    return render(request, 'blog_app/blog_details.html', {'blog': blog, 'comment_form': comment_form, 'liked': liked})
    
@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = Like(blog=blog, user=user)
        liked_post.save()
    
    return HttpResponseRedirect(reverse('blog_app:blog_details', kwargs={'slug':blog.slug}))

@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('blog_app:blog_details', kwargs={'slug':blog.slug}))

class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name = 'blog_app/edit_blog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog_app:blog_details', kwargs={'slug':self.object.slug})