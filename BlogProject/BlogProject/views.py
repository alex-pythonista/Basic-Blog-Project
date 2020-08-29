from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect

# views

def index(request):
    return HttpResponseRedirect(reverse('blog_app:blog_list'))