from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import Profile, Extended
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import jwt


# Create your views here.


def index(request):
    if request.method == 'POST':
        username = request.POST['us']
        email = request.POST['em']
        password = request.POST['ps']
        obj = Profile(username=username, email=email, password=password)
        obj.save()
        obj1 = Profile.objects.all()
        return redirect(reverse('index'), {'data': obj1})

        # return redirect(reverse('index'), )
    obj2 = Profile.objects.all()
    return render(request, 'index.html', {'data': obj2})


def home(request):
    return render(request, 'home.html')


def my_login(request):
    if request.method == 'POST':
        username = request.POST['us']
        password = request.POST['ps']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('admin_panel'))
        else:
            return render(request, 'login.html', {'message': 'Wrong username or password'})
    if request.user.is_authenticated:
        return redirect(reverse('admin_panel'),{'message': 'You are already logged in'})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['us']
        email = request.POST['em']
        password = request.POST['ps']
        file = request.FILES['img']


        try:
            user= User.objects.create_user(username=username, email=email, password=password, is_active=True)
            # enc = jwt.encode(payload={'userid': str(user.pk)} , key='atif', algorithm='HS512')
            # link= request.scheme+'://'+request.META['HTTP_HOST']+'/activation/'+str(enc)+'/'
            # em = EmailMessage('Your Account Created Successfully', 'Thanks for Registering your account on Xtreeme Tech! We are welcome to our site!. Please verify your email: '+link, 'atifayub788@gmail.com', [email])
            # em.send()
            img_obj = Extended()
            img_obj.id = user
            img_obj.img = file
            img_obj.save()
            return render(request, 'login.html', {'message': 'Please check your email to verify your account on Xtreeme Tech!'})
        except:
            return render(request, 'register.html', {'message': 'User Already Exist'})

    return render(request, 'register.html')


def activation(request, id):
    dec = jwt.decode(id, key='atif', algorithms=['HS512'])
    user = User.objects.get(pk=int(dec['userid']))
    user.is_active = True
    user.save()
    return render(request, 'login.html', {'message': 'Account was successfully activated'})


def my_logout(request):
    logout(request)
    return render(request, 'login.html')


def admin_panel(request):
    if request.user.is_authenticated:
        obj1 = Profile.objects.all()
        return render(request, 'admin_panel.html', {'data': obj1})
    else:
        return render(request, 'login.html', {'message': 'Plesae Login first to see your account'})


from .serializers import ProfileSerializer
from rest_framework.response import Response
from .models import Profile
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def serialize_data(request):
    if request.method == 'GET':
        all_data = Profile.objects.all()
        sr = ProfileSerializer(all_data, many=True)
        return Response(sr.data)

    if request.method == 'POST':
        data = request.data
        sr = ProfileSerializer(data=data)
        if sr.is_valid():
            sr.save()
            all_data = Profile.objects.all()
            sr = ProfileSerializer(all_data, many=True)
            return Response(sr.data)


import requests


def fetch_api_data(request):
    response = requests.get('http://127.0.0.1:8000/sdata/')
    data = response.json()
    return render(request, 'view_api.html', {'data': data})


