from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    blog_title = models.CharField(max_length=255, verbose_name="Put a title")
    slug = models.SlugField(max_length=255, unique=True)
    blog_content = models.TextField(verbose_name="What's on your mind?")
    blog_image = models.ImageField(upload_to='blog_images', verbose_name='Image')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date', ]

    def __str__(self):
        return self.blog_title

    def save(self):
        self.slug = slugify(self.blog_title)
        super(Blog, self).save()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date', ]

    def __str__(self):
        return self.comment

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='liked_blog')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_user')

    def __str__(self):
        return str(self.user) + " likes " + str(self.blog)