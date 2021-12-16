import smtplib
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode 
from datetime import datetime
from .models import UserModel

password_token = PasswordResetTokenGenerator()

def mailResetPasswordSuccessfully(user : User) -> None :
    fname = user.first_name
    uname = user.username
    email=user.email
    subject = "Password Reset for " + uname
    message = str(
    "<em>Dear {fname},\n</em>Your Password for account having <u><strong>username = {uname}</strong></u> has been changed on {date} successfully"
    .format(fname=fname,uname=uname,date=datetime.now().strftime("%A %d %B %Y "))
    )
    mail(email,subject,message)

def sendVerificationEmail(req:HttpRequest,user: User,userModel: UserModel):
    token = password_token.make_token(user=user)
    mail(user.email,"User Verification",render_to_string('email_temp.html',{
        'uid': str(userModel.id),
        'domain': get_current_site(req).domain,
        'token': token
        }))

def sendPasswordResetEmail(req:HttpRequest,user: User):
    mail(user.email,"Reset password",render_to_string('email_password_reset.html',{
        'uid': urlsafe_base64_encode(force_bytes(user.get_username())), 
        'domain': get_current_site(req).domain,
        'token': password_token.make_token(user=user),
        'user': user
        }))

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