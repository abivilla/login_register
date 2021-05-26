from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt


# Create your views here.

def index(request):
    return render (request,'login.html')

def success(request):
    if "user_id" not in request.session:
        return redirect('/')

    return render (request,'success.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if errors:
            for error in errors.values():
                messages.error(request,error)
            return redirect('/')

 
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
     
    
    user = User.objects.create(first_name=request.POST['first_name'],last_name = request.POST['last_name'],email = request.POST['email'], password=pw_hash) 
    
    request.session["user_id"] = user.id
    request.session["user_name"] = user.first_name
    return redirect('/success')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email)

        if user: 
            logged_user = user[0] 
       
            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
           
                request.session['user_id'] = logged_user.id
                request.session["user_name"] = logged_user.first_name
            
                return redirect('/success')
            else:
                messages.error(request,"This password is incorrect!")
                return redirect('/')
        else:
            messages.error(request,"This User doesn't exist!")
            return redirect('/')
    
    return redirect('/')

def logout(request):
    request.session.flush()

    return redirect('/')