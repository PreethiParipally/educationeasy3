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
from .models import Query,Answer
from appCourses.models import Course
from accounts.models import Faculty
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from discussionForum.templatetags import extras

@login_required
def search_queries(request,id):
    if request.method == "POST":
        searched = request.POST['searched']
        discussions = Query.objects.filter(course_id=id).filter(title__contains=searched)
        discussions_query = Query.objects.filter(course_id=id).filter(message__contains=searched)
        discussions= ( discussions | discussions_query).distinct()
        return render(request, 'discussions/search_queries.html', {'searched':searched,'discussions':discussions,'course_id':id})
    else:
        return render(request, 'discussions/search_queries.html', {'course_id':id})

@login_required
def viewDiscussions(request,id):
    if request.user.is_authenticated:
        discussions=Query.objects.filter(course_id=id)
        paginator = Paginator(discussions, 5) # Show 10 contacts per page.

        page_number = request.GET.get('page')
        discussions= paginator.get_page(page_number)
        page_obj= paginator.get_page(page_number)
        return render(request,'../templates/discussions/index.html',{'discussions':discussions,'page_obj': page_obj,'course_id':id})

# Create your views here.
@method_decorator(login_required, name='dispatch')
class AddQuery(CreateView):
    model = Query
    fields = ('title', 'question')
    template_name = 'discussions/addquery.html'
    extra_context = {
        'course_id': ''
    }

    def form_valid(self, form):
        query = form.save(commit=False)
        query.user = self.request.user
        query.course_id = self.kwargs['id']
        rank=0
        discussions=Query.objects.filter(course_id=self.kwargs['id'])
        for i in discussions:
          rank=max(rank,i.rank)
        query.rank = rank + 1
        query.save()
        discussions=Query.objects.filter(course_id=self.kwargs['id'])
        print(discussions)
        messages.success(self.request, 'The query was added with success! Go ahead!')
        return redirect('discussions:discussions',id=self.kwargs['id'])
    
    def get_context_data(self,*args, **kwargs):
        context = super(AddQuery, self).get_context_data(*args,**kwargs)
        context['course_id'] = self.kwargs['id']
        return context
        
@method_decorator(login_required, name='dispatch')
class UpdateQuery(UpdateView):
    model = Query
    fields = ('title', 'question' )
    context_object_name = 'query'
    template_name = 'discussions/updatequery.html'
    extra_context = {
        'course_id': ''
    }


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.queries.filter(course_id=self.kwargs['id']).all()

    def get_success_url(self):
        return reverse('discussions:query-detail',kwargs={'id':self.kwargs['id'],'pk': self.object.pk})

    def get_context_data(self,*args, **kwargs):
        context = super(UpdateQuery, self).get_context_data(*args,**kwargs)
        context['course_id'] = self.kwargs['id']
        return context


@method_decorator(login_required, name='dispatch')
class DeleteQuery(DeleteView):
    model = Query
    context_object_name = 'query'
    template_name = 'discussions/deletequery.html'
    extra_context = {
        'course_id': ''
    }

    def delete(self, request, *args, **kwargs):
        query = self.get_object()
        messages.success(request, 'The query %s was deleted with success!' % query.title)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.queries.filter(course_id=self.kwargs['id']).all()
      
    def get_success_url(self):
        return reverse_lazy('discussions:myqueries',kwargs={'id':self.kwargs['id']})

    def get_context_data(self,*args, **kwargs):
        context = super(DeleteQuery, self).get_context_data(*args,**kwargs)
        context['course_id'] = self.kwargs['id']
        return context

@login_required
def QueryDetailView(request,id, pk): 
    query=Query.objects.filter(course_id=id).filter(pk=pk).first()
    query.save()
        
    answers= Answer.objects.filter(query=query, parent=None).order_by('timestamp')
    replies= Answer.objects.filter(query=query).exclude(parent=None).order_by('timestamp')
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    # print(replyDict)
    context={'query':query, 'answers': answers, 'user': request.user, 'replyDict': replyDict}
    return render(request, "../templates/discussions/view_query.html", context)


# @method_decorator([login_required], name='dispatch')
# class UserPostList(ListView):
#     model = Query
#     context_object_name = 'posts'
#     template_name = 'discussions/user_posts.html'
#     paginate_by = 5

#     def get_queryset(self,*args,**kwargs):
#             user = User.objects.get(id=self.kwargs['pk'])
#             return Query.objects.filter(user=user)

@method_decorator(login_required, name='dispatch')
class ListQueries(ListView):
    model = Query
    context_object_name = 'queries'
    template_name = 'discussions/myqueries.html'
    paginate_by = 5
    extra_context = {
        'course_id': ''
    }

    def get_queryset(self):
        return Query.objects.filter(course_id=self.kwargs['id']).filter(user=self.request.user)
    
    def get_context_data(self,*args, **kwargs):
        context = super(ListQueries, self).get_context_data(*args,**kwargs)
        context['course_id'] = self.kwargs['id']
        return context



@login_required
def QueryAnswer(request,id,pk):
    if request.method == "POST":
        answer=request.POST.get('answer')
        user=request.user
        course=Course.objects.filter(id=id)
        query= Query.objects.filter(course_id=id).get(pk=pk)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            answer=Answer(answer = answer, user=user, course_id=id, query=query)
            answer.save()
            messages.success(request, "Your answer has been posted successfully")
        else:
            parent= Answer.objects.get(sno=parentSno)
            answer=Answer(answer= answer, user=user, course_id=id, query=query , parent=parent)
            answer.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect("discussions:query-detail",id=id,pk=pk)
