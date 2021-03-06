
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from decorators import faculty_required
from . import models
User = get_user_model()
from .models import Post, Comment
from accounts.models import Faculty
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from posts.templatetags import extras

def search_posts(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)
        posts_message = Post.objects.filter(message__contains=searched)
        posts= ( posts | posts_message).distinct()
        return render(request, 'posts/search_posts.html', {'searched':searched,'posts':posts})
    else:
        return render(request, 'posts/search_posts.html', {})

def viewPosts(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        paginator = Paginator(posts, 5) # Show 10 contacts per page.

        page_number = request.GET.get('page')
        posts= paginator.get_page(page_number)
        page_obj= paginator.get_page(page_number)
        return render(request,'../templates/index.html',{'posts':posts,'page_obj': page_obj})
    return render(request, '../templates/home.html')

# Create your views here.
@method_decorator([login_required, faculty_required], name='dispatch')
class CreatePost(CreateView):
    model = Post
    fields = ('title', 'message', 'pdf')
    template_name = 'posts/addpost.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        messages.success(self.request, 'The post was created with success! Go ahead!')
        return redirect('index')
@method_decorator([login_required, faculty_required], name='dispatch')
class UpdatePost(UpdateView):
    model = Post
    fields = ('title', 'message','pdf' )
    context_object_name = 'post'
    template_name = 'posts/updatepost.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.posts.all()

    def get_success_url(self):
        return reverse('posts:post-detail', kwargs={'pk': self.object.pk})
@method_decorator([login_required, faculty_required], name='dispatch')
class DeletePost(DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/deletepost.html'
    success_url = reverse_lazy('posts:myposts')

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        messages.success(request, 'The post %s was deleted with success!' % post.title)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.posts.all()

# class PostDetailView(DetailView):
#     model = Post
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         post=self.get_object()
#         context['is_liked'] = False
#         context['is_favorite'] = False
#         context['total_likes']=post.total_likes()
#         if post.likes.filter(username=self.request.user).exists():
#             context['is_liked' ]= True

#         if post.favourite.filter(username=self.request.user).exists():
#             context['is_favourite'] = True
#         return context
@method_decorator([login_required], name='dispatch')
class UserPostList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/user_posts.html'
    paginate_by = 5

    def get_queryset(self,*args,**kwargs):
            user = User.objects.get(id=self.kwargs['pk'])
            return Post.objects.filter(user=user)

@method_decorator([login_required, faculty_required], name='dispatch')
class ListPost(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/myposts.html'
    paginate_by = 5

    def get_queryset(self):
        self.user = User.objects.get(username=self.request.user)
        return Post.objects.filter(user=self.user)

@login_required
def favourite_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.favourite.filter(username=request.user).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(reverse('posts:post-detail',kwargs={'pk':pk}))


@login_required
def post_favourite_list(request):
    user = request.user
    favourite_posts = user.favorite.all()
    context = {
        'favourite_posts': favourite_posts,
    }
    return render(request, 'posts/post_favourite_list.html', context)


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(username=request.user).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('posts:post-detail',kwargs={'pk':pk}))

@login_required
def PostDetailView(request, pk): 
    post=Post.objects.filter(pk=pk).first()
    post.views= post.views +1
    post.save()
        
    comments= Comment.objects.filter(post=post, parent=None).order_by('timestamp')
    replies= Comment.objects.filter(post=post).exclude(parent=None).order_by('timestamp')
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    # print(replyDict)
    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    context['is_liked'] = False
    context['is_favorite'] = False
    context['total_likes']=post.total_likes()
    if post.likes.filter(username=request.user).exists():
        context['is_liked' ]= True

    if post.favourite.filter(username=request.user).exists():
        context['is_favourite'] = True
    return render(request, "../templates/posts/view_post.html", context)


@login_required
def postComment(request,pk):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        post= Post.objects.get(pk=pk)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=Comment(comment = comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= Comment.objects.get(sno=parentSno)
            comment=Comment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect("posts:post-detail",pk=pk)
