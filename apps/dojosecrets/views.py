from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from django.db.models import Q
from django.db.models import Count, Sum, Case, When, IntegerField

import datetime
import bcrypt
# Generate salt, and after use it in models.py too
# salt = bcrypt.gensalt()

from django.db.models import Count

from .models import User, Pokes
# Create your views here.
def index(request):
    context = {
        "users": User.objects.all()
    }
    if "id" in request.session:
        return redirect('/pokes')
    else:
        return render(request, 'dojosecrets/index.html', context)

def pokes(request):
    if "id" in request.session:

        context = {
            "user": User.objects.get(id=request.session['id']),
            "plikeme": Pokes.objects.annotate(total=Count("poker")).filter(poked=request.session['id']),
            # -------------------
            'users': User.objects.all().annotate(numpokes=Sum("pokes_recieved__pokes")).exclude(id=request.session['id']),
            # 'users': User.objects.all(),
            'users_debug': User.objects.all(),
            'pokes_debug': Pokes.objects.all(),
            # -------------------
            'youPoked':Pokes.objects.all().filter(poked=request.session['id']),

            #
            #
            # "greg_query": Poke.objects.values("poker__first_name", "poker__last_name").annotate(total=Count("poker")).order_by('total').filter(poked__id = user_id)
            # {% for x in poked_num %}
            # {{ x.poker__first_name }} {{ x.poker__last_name }} {{ x.total }}
            # {% endfor %}

            #
        }
        return render(request, 'dojosecrets/success.html', context)
    else:
        return redirect("/")

def poke(request, id):
    poker_id = request.session['id']
    poked_user_id = id
    User.objects.poke(poker_id, poked_user_id)
    return redirect('/pokes')


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

                return redirect('/pokes')

        return redirect('/')

def reg(request):
    if request.method == "POST":
        fname = request.POST['fname']
        alias = request.POST['alias']
        email = request.POST['email']
        pw = request.POST['pw']
        repw = request.POST['repw']
        b_date = request.POST['bdate']

        answer = User.objects.reg(fname,alias,email,pw,repw,b_date)

        if not answer['fname'] or not answer['alias']:
            messages.add_message(request, messages.ERROR, 'Please enter string at least 3 characters in Name and Alias fields')
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
                fname=fname,
                alias=alias,
                email=email,
                password=hashed_pw,
                dateOfBirth=formated
            )

            request.session['id'] = User.objects.get(email=email).id

            messages.add_message(request, messages.SUCCESS, "Successfully registered!")
            return redirect('/pokes')

    return redirect('/')
