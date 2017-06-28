from __future__ import unicode_literals

from django.db import models

import datetime
import bcrypt

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

    def reg(self,fname,alias,email,pw,repw,b_date):
        print fname,alias,email,pw,repw
        f_name = True
        a_lias = True
        fl_name_alpha = True
        e_mail = True
        pw_length = True
        pw_match = True
        e_mail_uniq = True
        b_date_flag = True

        if len(fname)<2:
            f_name = False
        elif len(alias)<2:
            a_lias = False
        elif len(b_date)<9:
            b_date_flag = False
        else:
            # date validation
            try:
                formated = datetime.datetime.strptime(b_date, "%Y-%m-%d")
            except:
                b_date_flag = False

            # is alphabetical string was imput
            if not str(fname).isalpha() or not str(alias).isalpha():
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
            'fname': f_name,
            'alias': a_lias,
            'fl_alpha': fl_name_alpha,
            'email': e_mail,
            'pw_length': pw_length,
            'pw_match': pw_match,
            'uniq_email': e_mail_uniq,
            'b_date_flag': b_date_flag
        }

        return answer

    def poke(self,poker_id,poked_user_id):


        poker = User.objects.get(id=poker_id)
        if len(Pokes.objects.filter(poker=poker_id,poked_user=poked_user_id)) > 0:
            numPokes = Pokes.objects.get(poker=poker_id,poked_user=poked_user_id)
            numPokes.pokes = int(numPokes.pokes) + 1
            numPokes.save()
        else:
            Pokes.objects.create(pokes="1",poked_user=poked_user_id,poker=poker)
        return ''


class User(models.Model):
    fname = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    dateOfBirth = models.DateTimeField()

    objects = userManager()

class Pokes(models.Model):
    pokes = models.IntegerField(default='0')
    poked_user = models.IntegerField(default='0')
    poker = models.ForeignKey(User, related_name="poker_id")





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
