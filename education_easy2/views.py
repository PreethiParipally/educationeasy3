from django.shortcuts import render
from posts.models import Post
from django.core.paginator import Paginator

def index(request):
    return render(request, '../templates/home.html')
  

      
