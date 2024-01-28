from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required
# - authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
# - mail
from django.core.mail import send_mail
from django.conf import settings

def homepage(request):
    return render(request, 'lap/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # - send mail
            user_email = form.cleaned_data.get('email')
            user_password = form.cleaned_data.get('password2')
            subject = 'Welcome to Lap'
            message = f'Your account has been created.\n\nEmail: {user_email}\nPassword: {user_password}\n\nHope you are enjoying your Django our Services. Thank you for choosing us.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_email]
            send_mail(subject, message, email_from, recipient_list)
            
            return redirect("my-login")
    context = {'registerForm': form}
    return render(request, 'lap/register.html', context=context)

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # - authenticate the user
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {'loginForm': form}
    return render(request, 'lap/my-login.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='my-login')
def dashboard(request):
   return render(request, 'lap/dashboard.html')

# def send_email_to_new_user(request):
    