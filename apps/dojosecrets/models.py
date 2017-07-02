from __future__ import unicode_literals

from django.db import models

import pytz, datetime, bcrypt
from datetime import date
from django.utils.timezone import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

todaySalt = ''
todayDate = ''


# Create your models here.
class userManager(models.Manager):
    def login(self,email,pw):
        e_mail = True
        pw_match = True
        empty = True

        user = ''

        if len(email) < 2 or len(pw) < 2:
            empty = False
        else:
            query = User.objects.filter(email=email)
            if len( query ) == 0:
                e_mail = False
            else:

                db_hashed = query[0].password

                if db_hashed != bcrypt.hashpw(pw.encode(), db_hashed.encode()):
                    pw_match = False
                else:
                    user = User.objects.get(email=email)

        answer = {
            "email": e_mail,
            "pwmatch": pw_match,
            "empty": empty,
            "user": user
        }
        return answer

    def reg(self,name,email,pw,repw,b_date):
        print name,email,pw,repw
        f_name = True
        a_lias = True
        fl_name_alpha = True
        e_mail = True
        pw_length = True
        pw_match = True
        e_mail_uniq = True
        b_date_flag = True

        if len(name)<2:
            f_name = False
        elif len(b_date)<9:
            b_date_flag = False
        else:
            # date validation
            try:
                formated = datetime.datetime.strptime(b_date, "%Y-%m-%d")
            except:
                b_date_flag = False

            # is alphabetical string was imput
            if not str(name).isalpha():
                fl_name_alpha = False

            # email validation
            try:
                validate_email(email)
            except:
                e_mail = False

            # the same emails
            if len(User.objects.filter(email=email))>0:
                e_mail_uniq = False

            # password match
            if pw != repw:
                pw_match = False
            if len(pw)<8:
                pw_length = False

        answer = {
            'name': f_name,
            'fl_alpha': fl_name_alpha,
            'email': e_mail,
            'pw_length': pw_length,
            'pw_match': pw_match,
            'uniq_email': e_mail_uniq,
            'b_date_flag': b_date_flag
        }

        return answer

    def makeAppointemt(self,user_id,date,time,task):
        d_ate = True
        t_ime = True
        t_ask = True
        d_ate_mssg = "Please enter date in correct format"

        if not len(date) == 10:
            d_ate = False
        elif not len(time) == 5:
            t_ime = False
        elif len(task) < 2:
            t_ask = False
            print 'false'
        else:
            # date validation
            fulldate = date + "-" + time
            print fulldate

            try_formatdate = False

            try:
                formated = datetime.strptime(fulldate, "%Y-%m-%d-%H:%M")
                print 'striptime SUCCESS'
                try_formatdate = True
            except:
                d_ate = False
                print "failed"

            if try_formatdate:
                today = datetime.today()
                if formated < today:
                    d_ate = False
                    d_ate_mssg = "Please enter today's date"
                # if formated.day < today.day:
                #     d_ate = False
                #     d_ate_mssg = "Please enter today's date"
                # elif formated.hour < today.hour:
                #     d_ate = False
                #     d_ate_mssg = "Please enter hours in future "
                # elif  formated.day <= today.day and formated.hour <= today.hour and formated.minute < today.minute:
                #     d_ate = False
                #     d_ate_mssg = "Please enter minutes in future"
                else:
                    user = User.objects.get(id=user_id)
                    Appointment.objects.create(user=user,status="Pending",task=task,date=formated)




        answer = {
            "d_ate": d_ate,
            "t_ime": t_ime,
            "d_ate_false": d_ate_mssg,
            "t_ask": t_ask,
            "t_ask_false": "Please fill out task field",
            "success":"New appointment was created"
        }
        return answer

    def editAppinment(self,app_id,status,date,time,task,user_id):
        d_ate = True
        t_ime = True
        t_ask = True
        d_ate_mssg = "Please enter date in correct format"

        if not len(date) == 10:
            d_ate = False
        elif not len(time) == 5:
            t_ime = False
        elif len(task) < 2:
            t_ask = False
            print 'false'
        else:
            # date validation
            fulldate = date + "-" + time
            print fulldate

            try_formatdate = False
            today = datetime.today()

            try:
                formated = datetime.strptime(fulldate, "%Y-%m-%d-%H:%M")
                print 'striptime SUCCESS'
                print formated.minute
                print today.minute
                try_formatdate = True
            except:
                d_ate = False
                print "failed"

            if try_formatdate:
                if formated < today:
                    d_ate = False
                    d_ate_mssg = "Please enter today's date"
                # if formated.day < today.day:
                #     d_ate = False
                #     d_ate_mssg = "Please enter today's date"
                # elif formated.hour < today.hour:
                #     d_ate = False
                #     d_ate_mssg = "Please enter hours in future "
                # elif  formated.day <= today.day and formated.hour <= today.hour and formated.minute < today.minute:
                #     d_ate = False
                #     d_ate_mssg = "Please enter minutes in future"
                else:
                    user = User.objects.get(id=user_id)
                    ApptmentSelect = Appointment.objects.get(id=app_id)
                    ApptmentSelect.status=status
                    ApptmentSelect.task=task
                    ApptmentSelect.date=formated
                    ApptmentSelect.save()




        answer = {
            "d_ate": d_ate,
            "t_ime": t_ime,
            "d_ate_false": d_ate_mssg,
            "t_ask": t_ask,
            "t_ask_false": "Please fill out task field",
            "success":"New appointment was created"
        }
        return answer

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    dateOfBirth = models.DateTimeField()

    objects = userManager()

class Appointment(models.Model):
    task = models.CharField(max_length=250)
    status = models.CharField(max_length=100)
    date = models.DateTimeField()

    user = models.ForeignKey(User, related_name="user")

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)





    # def mss(self, id):
    #     checkToday = str(datetime.datetime.now().strftime('%D'))
    #     global todayDate
    #     global todaySalt
    #
    #     if todayDate != checkToday:
    #         todayDate = checkToday
    #         print todayDate
    #         todaySalt = bcrypt.gensalt()
    #         print todaySalt
    #     # if
    #
    # def esalt(self, id):
    #     self.mss(id)
    #     email = User.objects.get(id=id).email
    #     return bcrypt.hashpw(email.encode(), todaySalt)
    #     #  if expireTime != expireTime
    #
    # def trueSession(self,id,key):
    #     self.mss(id)
    #     if len( User.objects.filter(id=id) ) > 0:
    #         email = User.objects.get(id=id).email
    #         hashedEmail = bcrypt.hashpw(email.encode(), todaySalt)
    #         if key == hashedEmail:
    #             return True
    #         else:
    #             return False
