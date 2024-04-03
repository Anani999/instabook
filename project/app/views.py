from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('feed')  # Replace 'feed' with the URL name of your feed page
        return view_func(request, *args, **kwargs)
    return wrapper


def empty(request):
    return redirect('login')

@redirect_authenticated_user
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(request , username=username,password=password)
        if user != None:
            login(request,user)
            return redirect('profile-settings')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login_view')
    else:
        return render(request , 'login.html')

@redirect_authenticated_user
def signup(request):

    if request.user.is_authenticated():
        return redirect('feed')

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')


        if pass1 == pass2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=pass1)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                return redirect('login')
            else:
                messages.error(request,'user already exist !')
                return redirect('signup')
        else:
            messages.error(request,'Password mismatch !')
            return redirect('signup')
    else:
        return render(request ,'signup.html')



@login_required
def profile_settings(request):
    profile = Profile.objects.filter(user=request.user)
    return render(request , 'profile_settings.html', {'profile':profile})

@login_required
def feed(request):
    return HttpResponse('feed view')

@login_required
def profile(request):
    return HttpResponse('profile view')

def logout_view(request):
    logout(request)
    return HttpResponse('Logout success !')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)




# Create your views here.s
