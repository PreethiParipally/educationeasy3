from datetime import datetime, timedelta, date

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from django.urls import reverse,reverse_lazy
from .forms import SearchForm
from .models import *
from schedular.models import Schedule,UserBook
from .utils import Calendar
import jdatetime
from hijri_converter import convert

from typing import Counter
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from decorators import faculty_required,student_required

User = get_user_model()
from appCourses.models import Course


@method_decorator([login_required, faculty_required], name='dispatch')
class CalendarView(generic.ListView):
    model = Schedule
    template_name = '../templates/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user,withyear=True)
        
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['year'] = datetime.today().year
        context['month'] = datetime.today().month
        context['day'] = datetime.today().day
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
    
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
    

# def schedule(request, schedule_id=None):
#     instance = schedule()
#     if schedule_id:
#         instance = get_object_or_404(schedule, pk=schedule_id)
#     else:
#         instance = schedule()
    
#     form = scheduleForm(request.POST or None, instance=instance)
#     if request.POST and form.is_valid():
#         form.save()
#         return HttpResponseRedirect(reverse('cal:calendar'))
#     return render(request, 'cal/schedule.html', {'form': form})
    
# def schedule_search(request):
#     form = SearchForm()
#     query = None
#     resaults = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             resaults = schedule.objects.filter(title__contains=query) or schedule.objects.filter(body__contains=query) or schedule.objects.filter(author__contains=query)
#     return render(request, 'cal/search.html', {'form': form, 'query': query, 'resaults': resaults})
