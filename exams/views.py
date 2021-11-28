from typing import Counter
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from decorators import faculty_required,student_required
User = get_user_model()
from .models import Exam,Question,Result
from appCourses.models import Course
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

# Create your views here.

@method_decorator([login_required, faculty_required], name='dispatch')
class ListFacultyCourseExams(ListView):
  model = Exam
  context_object_name = 'exams'
  template_name = '../templates/faculty/exams.html'
  extra_context = {
        'course_id': '',
        'count' : 0
    }
  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])
  
  def get_context_data(self,*args, **kwargs):
    context = super(ListFacultyCourseExams, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    context['count'] = self.model.objects.filter(course_id=self.kwargs['id']).count()
    questions= Question.objects.filter()
    return context

@login_required
@faculty_required
def view_results(request,id1,id2):
  course=Course.objects.get(id=id1)
  exam=Exam.objects.get(id=id2)
  results= Result.objects.all().filter(course=course).filter(exam=exam)
  count = Result.objects.all().filter(course=course).filter(exam=exam).count()
  return render(request,'../templates/faculty/view_results.html',{'results':results,'count':count,'course':course,'exam':exam})


@method_decorator([login_required, faculty_required], name='dispatch')
class AddExam(CreateView):
  model = Exam
  fields = ('exam_name',)
  template_name = '../templates/faculty/addexam.html'
  context_object_name = 'exam'
  extra_context = {
        'course_id': ''
    }
  def get_success_url(self):
    messages.success(self.request, 'The exam was created with success! Go ahead!')
    return reverse('exams:exams', kwargs={'id': self.kwargs['id']})

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.course_id = self.kwargs['id']
    return super().form_valid(form)

  def get_context_data(self,*args, **kwargs):
    context = super(AddExam, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class ViewExam(ListView):
  model = Question
  context_object_name = 'questions'
  template_name = '../templates/faculty/view_exam.html'
  extra_context = {
        'course_id': '',
        'assignment_id':'',
        'count':0
    }
  def get_queryset(self):
    return self.model.objects.filter(exam_id=self.kwargs['id2']).filter(course_id=self.kwargs['id1'])
  
  def get_context_data(self,*args, **kwargs):
    context = super(ViewExam, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['exam_id'] = self.kwargs['id2']
    context['count'] = self.model.objects.filter(exam_id=self.kwargs['id2']).filter(course_id=self.kwargs['id1']).count()
    return context


@method_decorator([login_required, faculty_required], name='dispatch')
class UpdateExam(UpdateView):
  model = Exam
  fields = ('exam_name',)
  context_object_name = 'exam'
  template_name = '../templates/faculty/update_exam.html'
  extra_context = {
        'course_id': ''
    }

  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])

  def get_success_url(self):
    return reverse('exams:exams', kwargs={'id':self.kwargs['id']})

  def get_context_data(self,*args, **kwargs):
    context = super(UpdateExam, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class DeleteExam(DeleteView):
  model = Exam
  context_object_name = 'exam'
  template_name = '../templates/faculty/delete_exam.html'
  extra_context = {
        'course_id': ''
    }

  def delete(self, request, *args, **kwargs):
    exam = self.get_object()
    messages.success(request, 'The exam was deleted with success!')
    return super().delete(request, *args, **kwargs)

  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])
  
  def get_success_url(self):
    return reverse('exams:exams', kwargs={'id':self.kwargs['id']})

  def get_context_data(self,*args, **kwargs):
    context = super(DeleteExam, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class AddQuestion(CreateView):
  model = Question
  fields = ('marks','question','option1','option2','option3','option4','answer')
  template_name = '../templates/faculty/add_question.html'
  context_object_name = 'question'
  extra_context = {
        'course_id': '',
        'exam_id':''
    }
  def get_success_url(self):
    messages.success(self.request, 'The question was created with success! Go ahead!')
    return reverse('exams:view_exam', kwargs={'id1': self.kwargs['id1'],'id2':self.kwargs['id2']})

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.course_id = self.kwargs['id1']
    form.instance.exam_id = self.kwargs['id2']
    return super().form_valid(form)

  def get_context_data(self,*args, **kwargs):
    context = super(AddQuestion, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['exam_id'] = self.kwargs['id2']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class UpdateQuestion(UpdateView):
  model = Question
  fields = ('marks','question','option1','option2','option3','option4','answer')
  context_object_name = 'question'
  template_name = '../templates/faculty/update_question.html'
  extra_context = {
        'course_id': '',
        'exam_id':''
    }
  
  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id1']).filter(exam_id=self.kwargs['id2'])

  def get_success_url(self):
    return reverse('exams:view_exam', kwargs={'id1': self.kwargs['id1'],'id2':self.kwargs['id2']})

  def get_context_data(self,*args, **kwargs):
    context = super(UpdateQuestion, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['exam_id'] = self.kwargs['id2']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class DeleteQuestion(DeleteView):
  model = Question
  context_object_name = 'question'
  template_name = '../templates/faculty/delete_question.html'
  extra_context = {
        'course_id': '',
        'exam_id':''
    }

  def delete(self, request, *args, **kwargs):
    question = self.get_object()
    messages.success(request, 'The question was deleted with success!')
    return super().delete(request, *args, **kwargs)

  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id1']).filter(exam_id=self.kwargs['id2'])
  
  def get_success_url(self):
    return reverse('exams:view_exam', kwargs={'id1': self.kwargs['id1'],'id2':self.kwargs['id2']})

  def get_context_data(self,*args, **kwargs):
    context = super(DeleteQuestion, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['exam_id'] = self.kwargs['id2']
    return context

@method_decorator([login_required, student_required], name='dispatch')
class ListStudentCourseExams(ListView):
  model = Exam
  context_object_name = 'exams'
  template_name = '../templates/student/exams_student.html'
  extra_context = {
        'course_id': '',
        'count':0
    }
  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])
  
  def get_context_data(self,*args, **kwargs):
    context = super(ListStudentCourseExams, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    context['count'] = self.model.objects.filter(course_id=self.kwargs['id']).count()
    return context

@login_required
@student_required
def take_exam_view(request,id,pk):
    course=Course.objects.get(id=id)
    exam=Exam.objects.get(id=pk)
    total_questions=Question.objects.all().filter(exam=exam).count()
    questions=Question.objects.all().filter(exam=exam)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    is_taken=Result.objects.filter(course_id=id).filter(exam_id=pk).filter(user=request.user).count()
    return render(request,'../templates/student/take_exam.html',{'course':course,'exam':exam,'total_questions':total_questions,'total_marks':total_marks,'is_taken':is_taken})

@login_required
@student_required
def start_exam_view(request,id,pk):
    course=Course.objects.get(id=id)
    exam=Exam.objects.get(id=pk)
    questions=Question.objects.all().filter(exam=exam)
    count=Question.objects.all().filter(exam=exam).count()
    if(count==0):
      return render(request,'../templates/student/no_questions.html')
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    if request.method=='POST':
        print("reached here")
        pass

    response= render(request,'../templates/student/start_exam.html',{'course':course,'exam':exam,'questions':questions})
    response.set_cookie('exam_id',exam.id)
    response.set_cookie('course_id',course.id)
    response.set_cookie('actual_marks',total_marks)
    return response


@login_required
@student_required
def calculate_marks_view(request,id):
    if request.COOKIES.get('exam_id') is not None:
        print(request.POST)
        course=Course.objects.get(id=id)
        exam_id = request.COOKIES.get('exam_id')
        exam=Exam.objects.get(id=exam_id)
        actual_marks=request.COOKIES.get('actual_marks')
        time = request.COOKIES.get('timer')
        print(request.COOKIES)
        total_marks=0
        correct=0
        wrong=0
        questions=Question.objects.all().filter(exam=exam)
        for i in range(len(questions)):
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
                correct+=1
            else:
                wrong+=1
        negative=int(time)//5
        total_marks=max(0,total_marks-negative)
        percent=total_marks*100//int(actual_marks)
        user = User.objects.get(id=request.user.id)
        result = Result()
        result.marks=total_marks
        result.exam=exam
        result.time_taken=time
        result.user=user
        result.course=course
        result.actual_marks=actual_marks
        result.correct=correct
        result.wrong=wrong
        result.percent=percent
        result.save()
        return redirect('exams:view_result',id=id)


@login_required
@student_required
def view_result_view(request,id):
    course=Course.objects.get(id=id)
    exams=Exam.objects.filter(course_id=id)
    count=Exam.objects.filter(course_id=id).count()
    return render(request,'../templates/student/view_result.html',{'exams':exams,'count':count,'course':course})
    

@login_required
@student_required
def check_marks_view(request,id,pk):
  course=Course.objects.get(id=id)
  exam=Exam.objects.get(id=pk)
  user = User.objects.get(id=request.user.id)
  results= Result.objects.all().filter(course=course).filter(exam=exam).get(user=user)
  count = Result.objects.all().filter(course=course).filter(exam=exam).filter(user=user).count()
  return render(request,'../templates/student/check_marks.html',{'results':results,'count':count,'course':course,'exam':exam})
