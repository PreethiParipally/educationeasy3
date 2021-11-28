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

import schedular
User = get_user_model()
from .models import Schedule,UserBook
from appCourses.models import Course
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.core import serializers
from django.http import JsonResponse
import json


from . import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.views import View
import urllib
from itertools import chain
from operator import attrgetter


# Create your views here.

@method_decorator(login_required, name='dispatch')
class ViewMySchedules(ListView):
  model = Schedule
  context_object_name = 'schedules'
  template_name = '../templates/my_schedules.html'
  extra_context = {
        'count' : 0
    }
  def get_queryset(self):
    return self.model.objects.filter(user=self.request.user)
  
  def get_context_data(self,*args, **kwargs):
    context = super(ViewMySchedules, self).get_context_data(*args,**kwargs)
    context['count'] = self.model.objects.filter(user=self.request.user).count()
    return context

@login_required
@faculty_required
def CreatedScheduleDetailView(request,id, pk):
    course = get_object_or_404(Course, id=id)
    schedule = get_object_or_404(Schedule, pk=pk)
    return render(request, '../templates/faculty/view_schedule.html', {'course': course,'schedule':schedule})


@method_decorator(login_required, name='dispatch')
class ViewSchedules(ListView):
  model = Schedule
  context_object_name = 'schedules'
  template_name = '../templates/schedules.html'
  extra_context = {
        'course_id': '',
        'count' : 0
    }
  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])
  
  def get_context_data(self,*args, **kwargs):
    context = super(ViewSchedules, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    context['count'] = self.model.objects.filter(course_id=self.kwargs['id']).count()
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class AddSchedule(CreateView):
  model = Schedule
  fields = ('date','start_time','end_time','vaccine_dose','seats','students_per_row')
  template_name = '../templates/faculty/add_schedule.html'
  dict={}
  context_object_name = 'schedule'
  extra_context = {
        'course_id': ''
    }

  def get_success_url(self):
    messages.success(self.request, 'The schedule was created with success! Go ahead!')
    return reverse('schedular:schedules', kwargs={'id': self.kwargs['id']})

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.course_id = self.kwargs['id']
    added_schedules = models.Schedule.objects.filter(user_id=self.request.user.id)
    clash_array=[]
    flag=False
    for schedule in added_schedules:
    #######if the new schedule ends before or starts after the existing one then no clash#####
      if schedule.date!=form.instance.date or (schedule.start_time>=form.instance.end_time or schedule.end_time<=form.instance.start_time):
        continue
      else: 
        clash_array.append(schedule)
        flag=True
    if(flag):
      self.dict={'schedules':clash_array}
      messages.success(self.request, 'Your clashes with this schedule. Delete the following schedules to add this schedule!')
      return render(self.request, "../templates/faculty/clash_schedule.html", self.dict)
    return super().form_valid(form)

  def get_context_data(self,*args, **kwargs):
    context = super(AddSchedule, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class UpdateSchedule(UpdateView):
  model = Schedule
  fields = ('date','start_time','end_time','vaccine_dose','seats','students_per_row')
  template_name = '../templates/faculty/update_schedule.html'
  context_object_name = 'schedule'
  extra_context = {
        'course_id': ''
    }

  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])

  def get_success_url(self):
    return reverse('schedular:schedules', kwargs={'id':self.kwargs['id']})

  def get_context_data(self,*args, **kwargs):
    context = super(UpdateSchedule, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class DeleteSchedule(DeleteView):
  model = Schedule
  template_name = '../templates/faculty/delete_schedule.html'
  context_object_name = 'schedule'
  extra_context = {
        'course_id': ''
    }
  def delete(self, request, *args, **kwargs):
    schedule = self.get_object()
    messages.success(request, 'The schedule was deleted with success!')
    return super().delete(request, *args, **kwargs)

  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id'])
  
  def get_success_url(self):
    return reverse('schedular:schedules', kwargs={'id':self.kwargs['id']})

  def get_context_data(self,*args, **kwargs):
    context = super(DeleteSchedule, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id']
    return context

@method_decorator([login_required, faculty_required], name='dispatch')
class ViewBookings(ListView):
  model = UserBook
  context_object_name = 'bookings'
  template_name = '../templates/faculty/bookings.html'
  extra_context = {
        'course_id': '',
        'schedule_id': '',
        'count' : 0
    }
  def get_queryset(self):
    return self.model.objects.filter(schedule_id=self.kwargs['id2'])
  
  def get_context_data(self,*args, **kwargs):
    context = super(ViewBookings, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    context['schedule_id'] = self.kwargs['id2']
    context['count'] = self.model.objects.filter(schedule_id=self.kwargs['id2']).count()
    return context



#####################################################

@login_required
@student_required
def ScheduleDetailView(request,id, pk):
    course = get_object_or_404(Course, id=id)
    schedule = get_object_or_404(Schedule, pk=pk)
    is_booked = UserBook.objects.filter(user=request.user).filter(course=course).filter(schedule=schedule).count()
    seat = UserBook.objects.filter(user=request.user).filter(course=course).filter(schedule=schedule)
    print(seat,is_booked)
    if(seat):
      seat=seat.first()
    return render(request, '../templates/student/view_schedule.html', {'course': course,'schedule':schedule,'is_booked':is_booked,'seat':seat})


@method_decorator([login_required, student_required], name='dispatch')
class SelectSeat(ListView):
    template_name = "../templates/student/select_seat.html"
    model = Schedule
    from_class = forms.CheckEligibilityForm
    context_object_name="slot"
    extra_context = {
        'course_id': '',
        'schedule_id' : ''
    }

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            request.session['name'] = request.POST['name']
            request.session['dose'] = request.POST['dose']
            # request.session['file'] = request.POST['file']
            request.session['schedule_id'] = self.kwargs['id2']
            request.session['course_id'] = self.kwargs['id1']
            return redirect(reverse('schedular:book_seat'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id']= self.kwargs['id1']
        context['schedule_id']=self.kwargs['id2']
        return context

  

@method_decorator([login_required, student_required], name='dispatch')
class BookSeat(View):
    form_class = forms.BookedSeatForm
    initial = {'key': 'value'}
    dict={}
    template_name = "../templates/student/book_slot.html"
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        dd = '2021-02-02'     
        booking_seat = models.Schedule.objects.get(id=request.session['schedule_id'])
        # Sessions for schedule seat data ////////////////////////////////////////////////////////// 
        c_id  = request.session['course_id']
        s_id  = request.session['schedule_id']
        new_dict = {val:'0' for val in range(booking_seat.seats)}      
        ######################See if the student has eligible vaccination level#################################   
        if(int(request.session['dose'])<booking_seat.vaccine_dose) or (int(request.session['dose'])!=0 and int(request.session['dose'])!=1 and int(request.session['dose'])!=2):
          self.dict['eligible_vaccination']=booking_seat.vaccine_dose 
          self.dict['Your_vaccination_level']=int(request.session['dose'])
          messages.success(request, 'You have not at eligible vaccination level to book this schedule. Complete the eligible vaccination to book this slot!')
          return render(request, "../templates/student/not_eligible.html",self.dict)
        ####################See if the student is available for this particular schedule##########################
        booked_seats = models.UserBook.objects.filter(user_id=request.user.id)
        clash_array=[]
        flag=False
        for seat in booked_seats:
          #######if the new schedule ends before or starts after the existing one then no clash#####
          if seat.schedule.date!=booking_seat.date or (seat.schedule.start_time>=booking_seat.end_time or seat.schedule.end_time<=booking_seat.start_time):
            continue
          else: 
            clash_array.append(seat)
            flag=True
        if(flag):
          self.dict={'seats':clash_array}
          messages.success(request, 'You have alreay booked a slot which clashes with this schedule. Cancel the previous booked slot to book this slot!')
          return render(request, "../templates/student/clash_slot.html", self.dict)
        ###########################See if previously any seats are booked for this particular schedule###################
        if models.UserBook.objects.filter(schedule_id=s_id).exists():      
            bookseats = models.UserBook.objects.filter(schedule_id=s_id) 
            print(bookseats)  
            for temp in bookseats:
              new_dict[str(temp.seat)] = 1
        rows=booking_seat.students_per_row
        cols= int(booking_seat.seats) // int(rows)
        rem_seats=0
        if(int(booking_seat.seats) % int(rows)!=0):
          rem_seats=int(booking_seat.seats) % int(rows)
        # print(rows,cols,rem_seats)
        print(new_dict)
        # new_dict = JsonResponse(new_dict)
        self.dict = {'seats':json.dumps(new_dict),'rows':rows,'cols':cols,'rem_seats':rem_seats}
        # json_response = JsonResponse(self.dict)
        return render(request, self.template_name, self.dict)

        

    def post(self, request, *args, **kwargs):  
        # form = self.form_class(request.POST)
        if request.method == 'POST':
            booked_seat = int(request.POST['booked_seat'])
            name = request.session['name']
            dose = request.session['dose']
            # file = request.session['file']  
            s_id  = request.session['schedule_id']  
            c_id =  request.session['course_id']  
            
           ############Saving booked seats data################
            if(booked_seat):
              obj = models.UserBook(user=request.user,schedule_id=s_id,course_id=c_id,name=name,vaccine_dose=dose,seat=booked_seat)
              obj.save()
              return redirect('schedular:schedules',id=c_id)
        return render(request, self.template_name, self.dict)



############ User will be able to see all his/her previous bookings done #################
class BookHistory(ListView):
    context_object_name = 'book_history'
    def get_queryset(self):
        return models.UserBook.objects.filter(user_id=self.request.user.id)
    template_name = "../templates/book_history.html"

################## User can download the ticket booked ##########################
class DownloadTicket(ListView):
    context_object_name = 'ticket_detail'

    def get_queryset(self):
        return models.UserBook.objects.filter(user_id=self.request.user.id)


    template_name = "../templates/download_ticket.html"

########### Single ticket download page################
class Ticket(DetailView):
    context_object_name = 'row'
    def get_queryset(self):
        return models.UserBook.objects.filter(user_id=self.request.user.id)
    template_name = "../templates/ticket.html"


@method_decorator(login_required, name='dispatch')
class CancelBooking(DeleteView):
  model = UserBook
  context_object_name = 'seat'
  template_name = '../templates/cancel_booking.html'
  extra_context = {
        'course_id': ''
    }

  def delete(self, request, *args, **kwargs):
    messages.success(request, 'The Booking was canceled with success!')
    return super().delete(request, *args, **kwargs)

  def get_queryset(self):
    return self.model.objects.filter(course_id=self.kwargs['id1'])
  
  def get_success_url(self):
    return reverse('schedular:schedules', kwargs={'id':self.kwargs['id1']})

  def get_context_data(self,*args, **kwargs):
    context = super(CancelBooking, self).get_context_data(*args,**kwargs)
    context['course_id'] = self.kwargs['id1']
    return context