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
email_token = PasswordResetTokenGenerator()

def mailResetPasswordSuccessfully(user : User) -> None :
    subject = "Password Reset for " + user.username
    message = render_to_string('email/email_passord_reset_successful.html',{'user':user,'date':datetime.now()})
    mail(user.email,subject,message)

def mailEmailResetSuccessfully(user: User) -> None:
    mail(user.email,"Email Changed for account "+user.get_username(),
    render_to_string('email/email_reset_successful.html', {'user':user, 'date':datetime.now()})
    )

def sendVerificationEmail(req:HttpRequest,user: User,userModel: UserModel):
    token = password_token.make_token(user=user)
    mail(user.email,"User Verification",render_to_string('email/email_temp.html',{
        'uid': str(userModel.id),
        'domain': get_current_site(req).domain,
        'token': token
        }))

def sendEmailResetEmail(req:HttpRequest,user:User, email:str):
    mail(email,"New Email verification",render_to_string('email/email-email-reset.html',{
        'uid': urlsafe_base64_encode(force_bytes(user.get_username())), 
        'email': urlsafe_base64_encode(force_bytes(email)),
        'domain': get_current_site(req).domain,
        'token': email_token.make_token(user=user),
        'user': user
    }))

def sendPasswordResetEmail(req:HttpRequest,user: User):
    mail(user.email,"Reset password",render_to_string('email/email_password_reset.html',{
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