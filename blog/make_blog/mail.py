from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from datetime import datetime
import smtplib
from .models import not_verified_user



def mailResetPassword(user : User) -> str :
    fname = user.first_name
    uname = user.username
    email=user.email
    subject = "Password Reset for " + uname
    message = str(
    "<em>Dear {fname},\n</em>Your Password for account having <u><strong>username = {uname}</strong></u> has been changed on {date} successfully"
    .format(fname=fname,uname=uname,date=datetime.now().strftime("%A %d %B %Y "))
    )
    mail(email,subject,message)

def sendVerificationEmail(req:HttpRequest,user: not_verified_user):
    mail(user.email,"User Verification",render_to_string('email_temp.html',{'uid': str(user.id), 'domain': get_current_site(req).domain}))

def mail(email:str,subject:str,message:str) -> None:
    try:
        from django.core.mail import send_mail
        successful = send_mail(subject,'','c@d.com',recipient_list=[email,],fail_silently= False,html_message=message)
        print('Mail Sent to '+ email if successful == 1 else 'Email send failed')
    except smtplib.SMTPSenderRefused as e:
        raise NotValidEmailException(email)
    except smtplib.SMTPException as e:
        print(e)
    except Exception as e:
        print(e)
        print('Error in mailing')

class NotValidEmailException(Exception):
    pass