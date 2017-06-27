from django.shortcuts import render, redirect
from django.contrib import messages

# new commetn
import bcrypt
# Generate salt, and after use it in models.py too
# salt = bcrypt.gensalt()

from .models import User, Secret
# Create your views here.
def index(request):
    context = {
        "users": User.objects.all()
    }
    if "id" in request.session:
        return redirect('secrets')
    else:
        return render(request, 'dojosecrets/index.html', context)



def login(request):
        if request.method == "POST":
            email = request.POST['email']
            pw = request.POST['pw']

            answer = User.objects.login(email,pw)

            if not answer['email']:
                messages.add_message(request, messages.ERROR, "We don't have such user with that email")
                return redirect('/')
            elif not answer['empty']:
                messages.error(request, "You can't enter empty or short value")
                return redirect('/')
            elif not answer['pwmatch']:
                messages.add_message(request, messages.ERROR, "The password you entered don't match this email")
                return redirect('/')
            elif  answer['user'] != '':
                messages.success(request, "Successfully logined!")
                request.session['fname'] = answer['user'].fname
                request.session['lname'] = answer['user'].lname
                request.session['id'] = answer['user'].id


                return redirect("secrets")

        return redirect('/')

def reg(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pw = request.POST['pw']
        repw = request.POST['repw']

        answer = User.objects.reg(fname,lname,email,pw,repw)

        if not answer['fname'] or not answer['lname']:
            messages.add_message(request, messages.ERROR, 'Please enter string at least 3 characters in Name and Lastname fields')
        elif not answer['fl_alpha']:
            messages.add_message(request, messages.ERROR, 'Use only alphabet characters')
        elif not answer['email']:
            messages.add_message(request, messages.ERROR, 'Email is not valid')
        elif not answer['pw_length']:
            messages.add_message(request, messages.ERROR, 'Password is too short')
        elif not answer['pw_match']:
            messages.add_message(request, messages.ERROR, "Passwords don't match")
        elif not answer['uniq_email']:
            messages.add_message(request, messages.ERROR, "We already have this email in data base")
        else:
            # if everything is good
            hashed_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

            User.objects.create(
                fname=fname,
                lname=lname,
                email=email,
                password=hashed_pw
            )

            # User.objects.mss(email)

            request.session['fname'] = fname
            request.session['lname'] = lname
            request.session['id'] = User.objects.get(email=email).id

            messages.add_message(request, messages.SUCCESS, "Successfully registered!")
            return redirect('secrets')

    return redirect('/')

def secrets(request):
    if request.method == "POST":
        pass
    else:
        if "id" in request.session:
            return render(request, 'dojosecrets/secrets.html')
        else:
            messages.error(request, "Sorry, your session is expired, login again")
            return redirect('/')

def top(request):
    pass

def deluser(request, id):
    User.objects.filter(id=id).delete()
    return redirect('/')

def logout(request):
    del request.session['id']
    return redirect('/')
