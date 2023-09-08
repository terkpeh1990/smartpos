from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.


def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        # create an instance the UserLoginForm in the form.py passing in request.Post or None as an argument
        form = UserLoginForm(request.POST)
        if form.is_valid():  # if the data passed to the UserLoginForm in the form.py is passes all the clean data methods
            # get the username form the already clearned data in UserLoginForm class in the form.py and store it into a varible called username
            username = form.cleaned_data.get('username')
            # get the password form the already clearned data in UserLoginForm class in the form.py and store it into a varible called password
            password = form.cleaned_data.get('password')
            # re-authenticate the username and password and store it into variable called user
            user = authenticate(username=username, password=password)
            type_obj = Profile.objects.get(user=user)
            print(type_obj.name)
            if user is not None:
                login(request, user)
                
                if user.is_authenticated and type_obj.is_new:
                    return redirect('change_password')
                elif user.is_authenticated and type_obj.is_standard:
                    return redirect ('production:manage_restock')
                else:
                    return redirect('accounts:dashboard')
                #if user passes the authentication and his object_type is == is_standard

            else:

                messages.info(request, 'Username or Password is incorrect')
                # redirect the user to the managers
                return redirect("log")


    context = {
        'form': form,  # context is the form itself
    }
    template= 'auth_accounts/login.html'
    return render(request, template, context)


def logout_request(request):
    logout(request)  # passout the request as an argument to the logout() function
    return redirect("log")  # redirect to the login page





def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            user.refresh_from_db()
            Profile.objects.create(user = user,name= user.first_name +" "+ user.last_name,is_standard=True ,is_new=True)
            messages.success(request,'User Created Successfully')
            return redirect('manage_profiles')

    template='auth_accounts/signup.html'
    context= {'form':form

    }
    return render(request,template, context)






def landing(request):
    template = 'landing.html'
    return render(request, template)



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            pro = request.user.id
            cc = Profile.objects.get(user=pro)
            cc.is_new = False
            cc.save()
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('log')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'auth_accounts/change_password.html', {
        'form': form
    })




def manage_profiles(request):
    profile = Profile.objects.all()
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            user.refresh_from_db()
            Profile.objects.create(user = user,name= user.first_name +" "+ user.last_name,is_standard=True ,is_new=True)
            messages.success(request,'User Created Successfully')
            return redirect('manage_profiles')
    else:
        form =CreateUserForm()

    template = 'auth_accounts/manage_profile.html'
    context ={
        'profile':profile,
        'form':form
    
    }
    return render(request,template,context)



def reset_staff_password(request,pk):
    profile = Profile.objects.get(id=pk)
    cc = "tempass@123"
    password = make_password(cc)
    staff = profile.user
    staff.password=password
    staff.save()
    profile.is_new = True
    profile.save()
    messages.success(request,'Password Reset Successful')
    return redirect('manage_profiles')