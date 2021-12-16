from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate, tokens
from django.db.models import Q
from django.http.request import HttpRequest, QueryDict
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render 
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from uuid import *
from .mail import mail, mailResetPasswordSuccessfully, sendPasswordResetEmail,sendVerificationEmail,password_token
from .models import Blog, BlogCategory, Comment, ContactClass, Images, UserModel
from .utils import *


ResultPerPage = 6
""" Configure how many query result you want to show in each page """

def index(req: HttpRequest):
    """Landing Page of website"""
    return render(req,'index.html')

def activate(req: HttpRequest, id:str, token):
    logout(req)
    try:
        userModel: UserModel = UserModel.objects.get(id=UUID(id))
        user: User = userModel.user
        if req.method == 'POST':
            if not password_token.check_token(user,token): return HttpResponseForbidden('Invalid Link')
            confirm_new_password = req.POST.get('confirm_new_password')
            new_password = req.POST.get('new_password')
            if not new_password or not confirm_new_password or new_password != confirm_new_password:
                return HttpResponseBadRequest('Invalid Passwords')
            user.set_password(new_password)
            user.is_active = True
            user.save()
            mail(user.email,"Account Activated", "Your Account has been activated successfully")
            login(request=req,user=user)
            return redirect('blogindex')
        return render(req,'activate.html',{'username': user.username, 'userImage': userModel.avatar_image, 'id':id, 'token': token})
    except User.DoesNotExist as e:
        return HttpResponseNotFound('Not Found')
    except UserModel.DoesNotExist as e:
        return HttpResponseBadRequest('Bad request')
    except Exception as e:
        return InternalServerError(e)

def blog(req: HttpRequest):
    """Endpoint to show blog list"""
    posted_blogs = Blog.objects.filter(blog_status='p').order_by('-blog_date')
    resultPage: Pages = paginateResults(req,posted_blogs,ResultPerPage,'blogvalue')
    blogs = []
    for blog in resultPage.listItem:
        blogs.append(blog)
    blogs = prettyFilter(blogs)
    return render(req,'blog.html',{'blogs' : blogs, 'pages': range(resultPage.pages), 'p': resultPage.p })

def blogpost(req: HttpRequest,id):
    """End point to view blog post"""
    try:
        blog_categories = BlogCategory.objects.all().order_by('-date')
        categories = []
        for cat in blog_categories[:6]:
            number_of_blogs = Blog.objects.filter(blog_category=cat,blog_status='p').count()
            cat.number = number_of_blogs
            categories.append(cat)
        blogPostItem: Blog = Blog.objects.get(blog_url=id)
        if blogPostItem.blog_status == 'p' :
            # comments = [item for item in Comment.objects.filter(post=blogPostItem).order_by('-timestamp')[:100]]
            comments = []
            for item in Comment.objects.filter(post=blogPostItem,parent=None).order_by('-timestamp')[:100]:
                try :
                    item.userImage = UserModel.objects.get(user=item.user).avatar_image
                except UserModel.DoesNotExist as e:
                    item.userImage = None
                item.replycomments = []
                for item2 in Comment.objects.filter(post=blogPostItem,parent=item).order_by('-timestamp')[:50]:
                    try :
                        item2.userImage = UserModel.objects.get(user=item2.user).avatar_image
                    except UserModel.DoesNotExist as e:
                        item2.userImage = None
                    item.replycomments.append(item2)
                comments.append(item)
            blog_desc = BeautifulSoup(blogPostItem.blog_content,"html.parser").get_text()
            blogPostItem.blog_date = pretty_date(blogPostItem.blog_date)
            try: 
                userModel: UserModel =  UserModel.objects.get(user=blogPostItem.blog_author)
                profileImage = userModel.avatar_image
                about_author = userModel.about
            except UserModel.DoesNotExist : 
                profileImage = None
                about_author = None
            return render(req,'blog-post.html',{ 'blog': blogPostItem, 'blog_desc': blog_desc, 'categories': categories, 'comments': comments, 'profileImage': profileImage, 'about_author': about_author })
        raise Http404("Page not found error")
    except:
        raise Http404("Page not found error")

def features(req: HttpRequest):
    return render(req,'features.html')

def pricing(req: HttpRequest):
    return render(req,'pricing.html')

def contact(req: HttpRequest):
    """Endpoint to get user questions"""
    if req.method == 'POST':
        credentials = req.POST
        contactDetails = ContactClass(query_desc=credentials.get('message'),customer_name=credentials.get('name'),customer_email=credentials.get('email'),query_subject=credentials.get('subject'), date = timezone.now())
        contactDetails.save()
        return HttpResponse('OK')
    return render(req,'contact.html')

def blog_single(req: HttpRequest):
    return render(req,'blog-single.html')

def category(req: HttpRequest,id):
    """Endpoint to list blogs according to their category"""
    posted_blogs = Blog.objects.filter(blog_category__category_url=id,blog_status='p').order_by('-blog_date')
    blogs = []
    results: Pages = paginateResults(req,posted_blogs,ResultPerPage,'blogcategoryvalue')
    for blog in results.listItem :
        blogs.append(blog)
    blogs = prettyFilter(blogs)
    return render(req,'blog.html',{'blogs' : blogs, 'pages': range(results.pages), 'p':  results.p })

def signUp(req :HttpRequest):
    """End to signup the user"""
    if req.method == 'POST':
        try:
            body = req.POST
            image_file = req.FILES.get('user_image')
            about = body.get('about')
            fname = body['firstName']
            lname = body['lastName']
            username = body['username']
            email = body['email']
            if not username.isalnum(): raise ValueError("Username must be alphanumeric")
            if not isEmail(email): raise ValueError("Enter a vaid email")
            if User.objects.get(Q(username=username)|Q(email=email)):
                return HttpResponseForbidden('User already exists')
        except User.DoesNotExist as e:
            try: 
                # If no user with this email and username save the user as not verified
                newUser : User = User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email)
                newUser.set_password('')
                newUser.is_active = False
                newUser.save()
                userModel : UserModel = UserModel.objects.create(user=newUser,avatar_image=image_file,about=about)
                userModel.save()
                ## email body to send
                sendVerificationEmail(req,newUser,userModel)
                #============end email============#
                return HttpResponse('OK')
            except Exception as e:
                return InternalServerError(e)
        except ValueError as e:
            return HttpResponseBadRequest(e)
        except Exception as e:
            return InternalServerError(e)
    return render(req,'signup.html') if not req.user.is_authenticated else redirect('blogindex')

def loginUser(req: HttpRequest):
    """End point to login a user"""
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(req,user)
            return redirect( req.POST.get('redirect') or req.META.get('HTTP_REFERER') or '/')
        else: return HttpResponseBadRequest('Incorrect Credentials')
    return render(req,'login.html') if not req.user.is_authenticated else redirect('/') 

def logoutUser(req: HttpRequest):
    """endpoint to logout an user"""
    logout(req)
    return redirect(req.META.get('HTTP_REFERER') or '/')

def search(req: HttpRequest):
    """Endpoint to paginate user"""
    qString = req.GET.get('q')
    results = []
    if qString != None and len(qString) != 0:
        result = Blog.objects.filter(blog_title__icontains=qString).order_by('-blog_date')
        results = [ item  for item in result]
        result = Blog.objects.filter(blog_content__icontains=qString).order_by('-blog_date')
        results.extend([item for item in result if item not in results])
        result = Blog.objects.filter(blog_author__username__icontains=qString).order_by('-blog_date')
        results.extend([item for item in result if item not in results])
        results : Pages = paginateResults(req,results or [],ResultPerPage,'blogsearch')
        return render(req, 'search.html', {'qs': qString or '' , 'blogs': prettyFilter(results.listItem), 'pages':range(results.pages), 'p': results.p })
    return render(req,'search.html',{})

def postComment(req: HttpRequest):
    """End point to post a comment"""
    if req.method == 'POST' and req.user.is_authenticated and req.POST.get('comment') is not None and req.POST.get('postId') is not None :
        try: 
            Text = req.POST['comment']
            user = req.user
            postId = req.POST['postId']
            ParentComment = None
            if req.POST.get('parentId') != None:
                try:
                    ParentComment: Comment = Comment.objects.get(id = req.POST.get('parentId'))
                    ParentComment = ParentComment.parent or ParentComment
                except Comment.DoesNotExist as e:
                    ParentComment = None
            post = Blog.objects.get(blog_id=postId)
            comment = Comment(Text=Text,user=user,post=post,parent=ParentComment)
            comment.save()
            return redirect(req.META.get('HTTP_REFERER') or '/')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Bad request")
    return redirect(req.META.get('HTTP_REFERER') or '/')

def userProfile(req: HttpRequest):
    """endpoint to update user profile"""
    if req.method == "GET":
        userImage = None
        if req.user.is_authenticated:
            userModel: UserModel = UserModel.objects.get(user=req.user)
            userImage = userModel.avatar_image if str(userModel.avatar_image) != '' else None
            userAbout = userModel.about or ''
        return render(req,'profile.html',{'userImage': userImage, 'userAbout': userAbout}) if req.user.is_authenticated else redirect('blogLogin')
    elif req.method == "POST" and req.user.is_authenticated:
        try:
            user: User = User.objects.get(username=req.user.username)
            postObject: QueryDict = req.POST
            requestedUsername = postObject.get('username')
            requestedImage = req.FILES.get('user_image')
            removeImage = postObject.get('removeImage')
            if requestedUsername and requestedUsername != req.user.username :
                try:
                    User.objects.get(username=requestedUsername)
                    return HttpResponseForbidden('Username is not available')
                except User.DoesNotExist as e:
                    user.username = requestedUsername
            if requestedImage != None or removeImage:
                try:
                    userModel: UserModel = UserModel.objects.get(user=req.user)
                    requestedImage = None if removeImage else ( requestedImage or userModel.avatar_image)
                    userModel.avatar_image = requestedImage
                    userModel.about = postObject.get('about') or userModel.about
                    userModel.save()
                except UserModel.DoesNotExist as e:
                    pass
            user.first_name = postObject.get('firstName') or user.first_name
            user.last_name = postObject.get('lastName') or user.last_name
            user.save()
            return redirect('blogindex')
        except Exception as e:
            return InternalServerError(e)
    else: return HttpResponseForbidden("Forbidden")

def resetPassword(req: HttpRequest):
    """endpoint to reset password"""
    if req.method == 'GET':
        if not req.user.is_authenticated:
            return redirect('blogindex')
        userImage = None
        try:
            userModel: UserModel = UserModel.objects.get(user = req.user)
            userImage = userModel.avatar_image
        except Exception as e:
            print(e)
            userImage = None
        return render(req,'reset-password.html', {'userImage':userImage, 'isResetLink': False})
    if req.method == 'POST':
        if not req.user.is_authenticated:
            return HttpResponseForbidden('You need to login to reset password')

        if not ( req.POST.get('password') and req.POST.get('new_password') and req.POST.get('confirm_new_password')):
            return HttpResponseBadRequest('Request not valid') 

        if req.POST['new_password'] != req.POST['confirm_new_password']: 
            return HttpResponseBadRequest('new password and confirm new password do not match')

        try: 
            user: User = User.objects.get(username = req.user.username)
            validate_password = authenticate(username=user.username,password=req.POST['password'])
            
            if validate_password == None:
                return HttpResponseForbidden('Invalid Credentials')
            
            user.set_password(req.POST['new_password'])
            user.save()
            mailResetPasswordSuccessfully(user)
            login(req,user)
            return redirect('blogindex')

        except User.DoesNotExist as e:
           return HttpResponseForbidden('User does not exists')
        except Exception as e:
            return InternalServerError(e)

def resetPasswordLink(req: HttpRequest, uid: str,token: str):
    from django.utils.encoding import force_text
    from django.utils.http import urlsafe_base64_decode 
    if req.method == 'GET':
        try:
            username = force_text(urlsafe_base64_decode(uid))
            user: User = User.objects.get(username=username)
           
        except User.DoesNotExist as e:
            return redirect('/')
        return (
            render(req,'reset-password.html', {'userImage': None, 'isResetLink': True, 'uid': uid, 'token':token})
        )

    if req.method == 'POST':
        try:
            username = force_text(urlsafe_base64_decode(uid))
            user: User = User.objects.get(username=username)
            if not password_token.check_token(user, token):
                return HttpResponseForbidden('Invalid Link')
            new_passsword = req.POST.get('new_password')
            confirm = req.POST.get('confirm_new_password')
            if  not new_passsword or not confirm or new_passsword != confirm:
                return HttpResponseBadRequest('Invalid request')
            if password_token.check_token(user, token):
                user.set_password(new_passsword)
                user.save()
                mailResetPasswordSuccessfully(user=user)
                return HttpResponse('Your Password has been reset successfully')
            else: return redirect('blogindex')
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            return HttpResponse('link is invalid!')
        except Exception as e:
            return InternalServerError(e)

def sendPasswordResetLink(req: HttpRequest):
    """Send Password resetlink for not logged in user"""
    if req.method == 'POST':
        if req.POST.get('cred') == None: return HttpResponseBadRequest("Bad Request")
        try:
            user: User = User.objects.get(Q(email=req.POST['cred'])| Q(username=req.POST['cred']))
            sendPasswordResetEmail(req,user)
            return redirect('/')
        except User.DoesNotExist as e:
            return HttpResponseBadRequest("User not found")
        except Exception as e:
            return InternalServerError(e)
    return render(req,'send_passwordreset_email_form.html')

@csrf_exempt
def uploadImage(request: HttpRequest):
    """endpoint to upload custom images"""
    if request.method == 'POST' and request.user.is_authenticated: # and str(request.headers['Origin']).split(':')[0] in ALLOWED_HOSTS:
        try:
            file = request.FILES.get('file') or request.FILES.get('image')
            product = Images.objects.create(image=file)
            product.save()
            return JsonResponse({'location': '/media/' + str(product.image)})
        except KeyError:
            return HttpResponseBadRequest("File not found")
        except Exception as e:
            return InternalServerError(e)
    if request.user.is_authenticated:
        return render(request,'s.html') 
    else:  raise Http404("Page not found")

def updateEmail(req :HttpRequest):
    return redirect('blogindex')