from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from django.db.models import Q
from django.db.models import Count, Sum, Case, When, IntegerField

import pytz, datetime, bcrypt
from datetime import date
from django.utils.timezone import datetime
# Generate salt, and after use it in models.py too
# salt = bcrypt.gensalt()

from django.db.models import Count

from .models import User, Appointment
# Create your views here.
def index(request):
    context = {
        "users": User.objects.all()
    }
    if "id" in request.session:
        return redirect('/appts')
    else:
        return render(request, 'dojosecrets/index.html', context)


def appts(request):
    if "id" in request.session:
        today = datetime.today()
        context = {
            "user": User.objects.get(id=request.session['id']),
            "apptmnts": Appointment.objects.all(),
            "apptstoday": Appointment.objects.all().filter(date__day=today.day)
            # datetime.timedelta(-1, 68400)
        }
        return render(request, 'dojosecrets/appointemts.html', context)
    else:
        return redirect("/")

def appt(request,id):
    if "id" in request.session:

        context = {
            'currAppintemt': Appointment.objects.get(id=id)
        }
        return render(request, 'dojosecrets/edit.html', context)
    else:
        return redirect("/")

def add_appt(request):
    if request.method == "POST":
        user_id = request.session['id']
        date = request.POST['date']
        time = request.POST['time']
        task = request.POST['task']
        print task

        answer = User.objects.makeAppointemt(user_id,date,time,task)

        if not answer['d_ate'] or not answer['t_ime']:
            messages.error(request, answer['d_ate_false'])
        elif not answer['t_ask']:
            messages.error(request, answer['t_ask_false'])
        else:
            messages.success(request, answer['success'])


        return redirect('/appts')
    else:
        return redirect('/appts')

def edit_appt(request):
    if request.method == "POST":
        print 'edit started'
        user_id = request.session['id']
        app_id = request.POST['id']
        status = request.POST['status']
        date = request.POST['date']
        time = request.POST['time']
        task = request.POST['task']
        print task

        answer = User.objects.editAppinment(app_id,status,date,time,task,user_id)

        if not answer['d_ate'] or not answer['t_ime']:
            messages.error(request, answer['d_ate_false'])
        elif not answer['t_ask']:
            messages.error(request, answer['t_ask_false'])
        else:
            messages.success(request, answer['success'])
            return redirect("/appts")

        url = '/appt/' + app_id

        return redirect(url)
    else:
        return redirect("/appts")


def delapptmt(request, id):
    Appointment.objects.filter(id=id).delete()
    return redirect('/')

def deluser(request, id):
    User.objects.filter(id=id).delete()
    return redirect('/')

def logout(request):
    del request.session['id']
    return redirect('/')

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
                request.session['id'] = answer['user'].id

                return redirect('/appts')

        return redirect('/')

def reg(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        pw = request.POST['pw']
        repw = request.POST['repw']
        b_date = request.POST['bdate']

        answer = User.objects.reg(name,email,pw,repw,b_date)

        if not answer['name']:
            messages.add_message(request, messages.ERROR, 'Please enter string at least 3 characters in Name field')
        elif not answer['b_date_flag']:
            messages.add_message(request, messages.ERROR, 'Insert please correct birth date')
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
            formated = datetime.datetime.strptime(b_date, "%Y-%m-%d")



            User.objects.create(
                name=name,
                email=email,
                password=hashed_pw,
                dateOfBirth=formated
            )

            request.session['id'] = User.objects.get(email=email).id

            messages.add_message(request, messages.SUCCESS, "Successfully registered!")
            return redirect('/appts')

    return redirect('/')
