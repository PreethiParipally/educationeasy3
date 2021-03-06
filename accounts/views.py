from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from .forms import StudentSignUpForm, FacultySignUpForm,UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Faculty
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from decorators import faculty_required
from posts.models import Post
from django.db.models import Count


def search_faculty(request):
    if request.method == "POST":
        searched = request.POST['searched']
        faculty_fname = User.objects.filter(first_name__contains=searched).filter(is_faculty=True)
        faculty_lname = User.objects.filter(last_name__contains=searched).filter(is_faculty=True)
        faculty_uname = User.objects.filter(username__contains=searched).filter(is_faculty=True)
        designation = User.objects.filter(faculty__designation__contains=searched).filter(is_faculty=True)
        faculty=(faculty_fname | faculty_lname | faculty_uname | designation).distinct()
        count=faculty.count()
        # faculty = User.objects.filter(username__contains=searched).filter(is_faculty=True)
        # count=faculty.count()
        
        return render(request, 'accounts/search_faculty.html', {'searched':searched,'faculty':faculty,'count':count})
    else:
        return render(request, 'accounts/search_faculty.html', {})

def search_student(request):
    if request.method == "POST":
        searched = request.POST['searched']
        student_fname = User.objects.filter(first_name__contains=searched).filter(is_student=True)
        student_lname = User.objects.filter(last_name__contains=searched).filter(is_student=True)
        student_uname = User.objects.filter(username__contains=searched).filter(is_student=True)
        student=(student_fname | student_lname | student_uname).distinct()
        count=student.count()
        # faculty = User.objects.filter(username__contains=searched).filter(is_faculty=True)
        # count=faculty.count()
        
        return render(request, 'accounts/search_student.html', {'searched':searched,'student':student,'count':count})
    else:
        return render(request, 'accounts/search_student.html', {})


def register(request):
    return render(request, 'accounts/register.html')

class student_register(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'accounts/student_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class faculty_register(CreateView):
    model = User
    form_class = FacultySignUpForm
    template_name = 'accounts/faculty_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'accounts/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def updateprofile(request):
    if(request.user.is_faculty):
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.faculty)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('accounts:profile',request.user.username)

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.faculty)
        posts=Post.objects.filter(user=request.user)
        total_posts=posts.count()
        no_likes=request.user.posts.aggregate(total_likes=Count('likes'))['total_likes']

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'total_posts':total_posts,
            'no_likes':no_likes
        }
    else:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.student)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('accounts:profile',request.user.username)

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.student)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        
    return render(request, 'accounts/updateprofile.html', context)

@login_required
def profile(request,username):
    user=get_object_or_404(User,username=username)
    if( user.is_faculty):
        posts=Post.objects.filter(user=user)
        total_posts=posts.count()
        no_likes=user.posts.aggregate(total_likes=Count('likes'))['total_likes']
        equal=0
        if user.username==request.user.username:
            equal=1
        return render(request,'accounts/profile.html',{'posts':posts,'equal':equal,'user':user,'total_posts':total_posts,'no_likes':no_likes})
    else:
        equal=0
        if user.username==request.user.username:
            equal=1
        return render(request,'accounts/profile.html',{'equal':equal,'user':user})
    

@login_required
def allfaculty(request):
    users = User.objects.filter(is_faculty=True)
    return render(request,'accounts/allfaculty.html',{'users': users})

@login_required
def allstudents(request):
    users = User.objects.filter(is_student=True)
    return render(request,'accounts/allstudents.html',{'users': users})
