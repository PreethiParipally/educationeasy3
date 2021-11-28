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
from django.views import View
from appCourses.forms import CourseAddForm
from decorators import faculty_required,student_required
from . import models
User = get_user_model()
from .models import Course,Assignment,AssignmentSubmission,RegisterCourse,Resource
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django import forms
# from django.core.exceptions import ValidationError
# Create your views here.

def search_courses(request):
    if request.method == "POST":
        searched = request.POST['searched']
        courses = Course.objects.filter(course_name__contains=searched)
        course_description = Course.objects.filter(course_description__contains=searched)
        faculty_details = Course.objects.filter(faculty_details__contains=searched)
        courses=(courses | course_description | faculty_details).distinct()
        return render(request, '../templates/courses/search_courses.html', {'searched':searched,'courses':courses})
    else:
        return render(request, '../templates/courses/search_courses.html', {})


def viewCourses(request):
  if request.user.is_authenticated:
    courses=Course.objects.all()
    paginator = Paginator(courses, 3) # Show 3 courses per page.

    page_number = request.GET.get('page')
    courses= paginator.get_page(page_number)
    page_obj= paginator.get_page(page_number)
    return render(request,'../templates/courses/courses.html',{'courses':courses,'page_obj': page_obj})
  return render(request, '../templates/home.html')

def CourseDetailView(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_registered = RegisterCourse.objects.filter(user=request.user).filter(course=course).count()
    return render(request, '../templates/courses/view_course.html', {'course': course,'is_registered':is_registered})

@method_decorator([login_required, student_required], name='dispatch')
class RegisterCourseView(CreateView):
  model = RegisterCourse
  fields = ()
  context_object_name = 'register_course'
  template_name = '../templates/courses/student/register_course.html'
  extra_context = {
        'course_id': ''
    }

  def get_success_url(self):
    messages.success(self.request, 'Successfully Registered to the Course! Go ahead!')
    return reverse('courses:courses')

  def form_valid(self, form):
    form.instance.user=self.request.user
    form.instance.course_id = self.kwargs['id']
    return super().form_valid(form)

  def get_context_data(self,*args, **kwargs):
    context = super(RegisterCourseView, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, student_required], name='dispatch')
class ListRegisteredCourses(ListView):
    model = RegisterCourse
    context_object_name = 'registered_courses'
    template_name = '../templates/courses/user_courses.html'
    paginate_by = 3
 
    

    def get_queryset(self):
        self.user = User.objects.get(username=self.request.user)
        return self.user.userregister.all()
        # return self.model.objects.filter(user=self.user)



@method_decorator([login_required, faculty_required], name='dispatch')
class ListCreatedCourses(ListView):
    model = Course
    #  
    context_object_name = 'courses'
    template_name = '../templates/courses/user_courses.html'
    paginate_by = 3

    def get_queryset(self):
        self.user = User.objects.get(username=self.request.user)
        return self.model.objects.filter(user=self.user)


# Create your views here.
@method_decorator([login_required, faculty_required], name='dispatch')
class CreateCourse(CreateView):
  model = Course
  fields = (
            'course_name',
            'course_image',
            'faculty_details',
            'course_description',
            'start_date',
            'end_date',
    )
  # from_class = CourseAddForm
  template_name = '../templates/courses/faculty/course_create.html'

  def form_valid(self, form):
    course = form.save(commit=False)
    course.user = self.request.user
    course.save()
    messages.success(self.request, 'The course was created with success! Go ahead!')
    return redirect('courses:courses')


@method_decorator([login_required, faculty_required], name='dispatch')
class UpdateCourse(UpdateView):
    model = Course
    fields = (
            'course_name',
            'course_image',
            'faculty_details',
            'course_description',
    )
    from_class = CourseAddForm
    context_object_name = 'course'
    template_name = '../templates/courses/faculty/updatecourse.html'
    extra_context = {
        'course_id': ''
    }

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.courses.all()

    def get_success_url(self):
        return reverse('courses:course-view', kwargs={'pk': self.object.pk})

    def get_context_data(self,*args, **kwargs):
        context = super(UpdateCourse, self).get_context_data(*args,**kwargs)
        context['course_id'] = self.kwargs['pk']
        return context


@method_decorator([login_required, faculty_required], name='dispatch')
class DeleteCourse(DeleteView):
    model = Course
    context_object_name = 'course'
    template_name = '../templates/courses/faculty/deletecourse.html'
    success_url = reverse_lazy('courses:mycreatedcourses')
    extra_context = {
        'course_id': ''
    }

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        messages.success(request, 'The course %s was deleted with success!' % course.course_name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.courses.all()

    def get_context_data(self,*args, **kwargs):
        context = super(DeleteCourse, self).get_context_data(*args,**kwargs)
        context['course_id'] = self.kwargs['pk']
        return context


@method_decorator(login_required, name='dispatch')
class ListCourseAssignments(ListView):
  model = Assignment
  context_object_name = 'assignments'
  template_name = '../templates/courses/assignments/assignments.html'
  extra_context = {
        'course_id': ''
    }
  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])
  
  def get_context_data(self,*args, **kwargs):
    context = super(ListCourseAssignments, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@login_required
@student_required
def AssignmentDetailView(request,id, pk):
    course = get_object_or_404(Course, id=id)
    assignment = get_object_or_404(Assignment, pk=pk)
    is_submitted = AssignmentSubmission.objects.filter(user=request.user).filter(course=course).filter(assignment=assignment).count()
    return render(request, '../templates/courses/assignments/student/view_assignment.html', {'course': course,'assignment':assignment,'is_submitted':is_submitted})


@method_decorator([login_required, faculty_required], name='dispatch')
class AddAssignment(CreateView):
  model = Assignment
  fields = ('title', 'content', 'marks')
  template_name = '../templates/courses/assignments/faculty/addassignment.html'
  context_object_name = 'assignment'
  extra_context = {
        'course_id': ''
    }
  def get_success_url(self):
    messages.success(self.request, 'The assignment was created with success! Go ahead!')
    return reverse('courses:assignments', kwargs={'id': self.kwargs['id']})

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.course_id = self.kwargs['id']
    return super().form_valid(form)

  def get_context_data(self,*args, **kwargs):
    context = super(AddAssignment, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class UpdateAssignment(UpdateView):
  model = Assignment
  fields = ('title', 'content', 'marks')
  context_object_name = 'assignment'
  template_name = '../templates/courses/assignments/faculty/updateassignment.html'
  extra_context = {
        'course_id': ''
    }

  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])

  def get_success_url(self):
    return reverse('courses:assignments', kwargs={'id':self.kwargs['id']})

  def get_context_data(self,*args, **kwargs):
    context = super(UpdateAssignment, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class DeleteAssignment(DeleteView):
  model = Assignment
  context_object_name = 'assignment'
  template_name = '../templates/courses/assignments/faculty/deleteassignment.html'
  extra_context = {
        'course_id': ''
    }

  def delete(self, request, *args, **kwargs):
    assignment = self.get_object()
    messages.success(request, 'The assignment %s was deleted with success!' % assignment.title)
    return super().delete(request, *args, **kwargs)

  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])
  
  def get_success_url(self):
    return reverse('courses:assignments', kwargs={'id':self.kwargs['id']})

  def get_context_data(self,*args, **kwargs):
    context = super(DeleteAssignment, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context


@method_decorator(login_required, name='dispatch')
class ListCourseResources(ListView):
  model = Resource
  context_object_name = 'resources'
  template_name = '../templates/courses/resources/resources.html'
  extra_context = {
        'course_id': ''
    }
  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])
  
  def get_context_data(self,*args, **kwargs):
    context = super(ListCourseResources, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context


@method_decorator([login_required, faculty_required], name='dispatch')
class AddResource(CreateView):
  model = Resource
  fields = ('title', 'file')
  context_object_name = 'resource'
  template_name = '../templates/courses/resources/add_resource.html'
  extra_context = {
        'course_id': ''
    }

  def get_success_url(self):
    messages.success(self.request, 'The resource was created with success! Go ahead!')
    return reverse('courses:resources', kwargs={'id': self.kwargs['id']})

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.course_id = self.kwargs['id']
    return super().form_valid(form)
  def get_context_data(self,*args, **kwargs):
    context = super(AddResource, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context


@method_decorator([login_required, faculty_required], name='dispatch')
class DeleteResource(DeleteView):
  model = Resource
  context_object_name = 'resource'
  template_name = '../templates/courses/resources/delete_resource.html'
  extra_context = {
        'course_id': ''
    }

  def delete(self, request, *args, **kwargs):
    resource = self.get_object()
    messages.success(request, 'The resource %s was deleted with success!' % resource.title)
    return super().delete(request, *args, **kwargs)

  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])
  
  def get_success_url(self):
    return reverse('courses:resources', kwargs={'id':self.kwargs['id']})

  def get_context_data(self,*args, **kwargs):
    context = super(DeleteResource, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class viewAssignmentSubmissions(ListView):
  model = AssignmentSubmission
  context_object_name = 'assignment_submissions'
  template_name = '../templates/courses/assignments/assignment_submissions.html'
  extra_context = {
        'course_id': '',
        'assignment_id':''
    }
  def get_queryset(self):
    return self.model.objects.filter(assignment_id=self.kwargs['id2'])
  
  def get_context_data(self,*args, **kwargs):
    context = super(viewAssignmentSubmissions, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['assignment_id'] = self.kwargs['id2']
    return context


@method_decorator([login_required, student_required], name='dispatch')
class viewMyAssignmentSubmission(ListView):
  model = AssignmentSubmission
  context_object_name = 'assignment_submissions'
  template_name = '../templates/courses/assignments/assignment_submissions.html'
  extra_context = {
        'course_id': '',
        'assignment_id':''
    }
  def get_queryset(self):
    return self.model.objects.filter(assignment_id=self.kwargs['id2']).filter(user_id=self.request.user.id)
  
  def get_context_data(self,*args, **kwargs):
    context = super(viewMyAssignmentSubmission, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['assignment_id'] = self.kwargs['id2']
    return context


@method_decorator([login_required, student_required], name='dispatch')
class AddAssignmentSubmissionView(CreateView):
  model = AssignmentSubmission
  fields = ('name', 'university_id', 'content', 'file')
  template_name = '../templates/courses/assignments/student/add_assignment_submission.html'
  context_object_name = 'assignment_submission'
  extra_context = {
        'course_id': '',
        'assignment_id':''
    }

  def get_success_url(self):
    messages.success(self.request, 'The assignment was submitted with success! Go ahead!')
    return reverse('courses:assignments', kwargs={'id': self.kwargs['id1']})

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.assignment_id = self.kwargs['id2']
    form.instance.course_id = self.kwargs['id1']
    return super().form_valid(form)

  def get_context_data(self,*args, **kwargs):
    context = super(AddAssignmentSubmissionView, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['assignment_id'] = self.kwargs['id2']
    return context

@method_decorator([login_required, student_required], name='dispatch')
class UpdateAssignmentSubmission(UpdateView):
  model = AssignmentSubmission
  fields = ('name', 'university_id', 'content', 'file')
  template_name = '../templates/courses/assignments/student/update_assignment_submission.html'
  context_object_name = 'assignment_submission'
  extra_context = {
        'course_id': '',
        'assignment_id':''
    }

  def get_queryset(self):
    # print(self.model.objects.filter(pk=self.kwargs['pk']))
    return self.model.objects.filter(assignment_id=self.kwargs['id2'])

  def get_success_url(self):
    return reverse('courses:my_assignment_submission', kwargs={'id1':self.kwargs['id1'],'id2':self.kwargs['id2']})

  def get_context_data(self,*args, **kwargs):
    context = super(UpdateAssignmentSubmission, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['assignment_id'] = self.kwargs['id2']
    return context

@method_decorator([login_required, student_required], name='dispatch')
class DeleteAssignmentSubmission(DeleteView):
  model = AssignmentSubmission
  template_name = '../templates/courses/assignments/student/delete_assignment_submission.html'
  context_object_name = 'assignment_submission'
  extra_context = {
        'course_id': '',
        'assignment_id':''
    }
  def delete(self, request, *args, **kwargs):
    assignment = self.get_object()
    messages.success(request, 'The assignment submission was deleted with success!')
    return super().delete(request, *args, **kwargs)

  def get_queryset(self):
    # print(self.model.objects.filter(course_id=self.kwargs['id1']))
    return self.model.objects.filter(course_id=self.kwargs['id1'])
  
  def get_success_url(self):
    return reverse('courses:assignments', kwargs={'id':self.kwargs['id1']})

  def get_context_data(self,*args, **kwargs):
    context = super(DeleteAssignmentSubmission, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['assignment_id'] = self.kwargs['id2']
    return context