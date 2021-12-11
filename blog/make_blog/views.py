from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http.request import HttpRequest, QueryDict
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Blog, BlogCategory, Comment, ContactClass, Images, UserModel
from .utils import *

ResultPerPage = 6

def index(req: HttpRequest):
    """Landing Page of website"""
    return render(req,'index.html')

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
            comments = [item for item in Comment.objects.filter(post=blogPostItem).order_by('-timestamp')[:100]]
            blog_desc = BeautifulSoup(blogPostItem.blog_content,"html.parser").get_text()[:120]
            blogPostItem.blog_date = pretty_date(blogPostItem.blog_date)
            try: profileImage = UserModel.objects.get(user=blogPostItem.blog_author).avatar_image
            except UserModel.DoesNotExist : profileImage = None
            return render(req,'blog-post.html',{ 'blog': blogPostItem, 'blog_desc': blog_desc, 'categories': categories, 'comments': comments, 'profileImage': profileImage })
        raise Http404("Page not found error 2")
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

def signUp(req: HttpRequest):
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
            password1 = body['password1']
            password2 = body['password2']
            isUserExists = User.objects.filter(username=username).exists()
            isEmailExists = User.objects.filter(email=email).exists()
            if username.isalnum() and not isUserExists and not isEmailExists and isEmail(email) and password1 == password2 :
                user: User = User.objects.create_user(username,email,password1)
                user.first_name = fname
                user.last_name = lname
                user.save()
                user_model: UserModel = UserModel.objects.create(user=user,avatar_image=image_file,about=about)
                user_model.save()
            elif not username.isalnum(): raise ValueError("Username must be alphanumeric")
            elif not isEmail(email): raise ValueError("Enter a vaid email")
            elif password1!=password2: raise ValueError("passwords donot match")
            elif isUserExists: raise NameError("User with this username already exists")
            elif isEmailExists: raise NameError("User with this email already exists")
        except ValueError as e: 
            return HttpResponseBadRequest(e)
        except NameError as e: 
            return HttpResponseForbidden(e)
        except Exception as e:
            return InternalServerError(e)
        return HttpResponse('OK')
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
            post = Blog.objects.get(blog_id=postId)
            comment = Comment(Text=Text,user=user,post=post,parent=None)
            comment.save()
            return redirect(req.META['HTTP_REFERER'] or '/')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Bad request")
    return redirect(req.META['HTTP_REFERER'] or '/')

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
            userImage: UserModel = UserModel.objects.get(user = req.user).avatar_image
            print(userImage)
        except Exception as e:
            print(e)
            userImage = None
        return render(req,'reset-password.html', {'userImage':userImage})
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
            login(req,user)
            return redirect('blogindex')

        except User.DoesNotExist as e:
           return HttpResponseForbidden('User does not exists')
        except Exception as e:
            return InternalServerError(e)

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