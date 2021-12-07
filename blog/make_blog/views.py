from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect, render
from django.utils import timezone
from bs4 import BeautifulSoup
from .models import Blog, BlogCategory, Comment, ContactClass, Images
from .utils import isEmail, pretty_date, prettyFilter, paginateResults

ResultPerPage = 6

def index(req):
    return render(req,'index.html')

def blog(req):
    posted_blogs = Blog.objects.filter(blog_status='p').order_by('-blog_date')
    resultPage = paginateResults(req,posted_blogs,ResultPerPage,'blogvalue')
    blogs = []
    for blog in resultPage.listItem:
        blogs.append(blog)
    blogs = prettyFilter(blogs)
    return render(req,'blog.html',{'blogs' : blogs, 'pages': range(resultPage.pages), 'p': resultPage.p })
def blogpost(req,id):
    try:
        blog_categories = BlogCategory.objects.all().order_by('-date')
        categories = []
        for cat in blog_categories[:6]:
            number_of_blogs = Blog.objects.filter(blog_category=cat,blog_status='p').count()
            cat.number = number_of_blogs
            categories.append(cat)
        blogPostItem = Blog.objects.get(blog_url=id)
        if blogPostItem.blog_status == 'p' :
            comments = [item for item in Comment.objects.filter(post=blogPostItem).order_by('-timestamp')[:100]]
            blog_desc = BeautifulSoup(blogPostItem.blog_content,"html.parser").get_text()[:120]
            blogPostItem.blog_date = pretty_date(blogPostItem.blog_date)
            return render(req,'blog-post.html',{ 'blog': blogPostItem, 'blog_desc': blog_desc, 'categories': categories, 'comments': comments })
        raise Http404("Page not found error 2")
    except:
        raise Http404("Page not found error")

def features(req):
    return render(req,'features.html')

def pricing(req):
    return render(req,'pricing.html')

def contact(req):
    if req.method == 'POST':
        credentials = req.POST
        contactDetails = ContactClass(query_desc=credentials.get('message'),customer_name=credentials.get('name'),customer_email=credentials.get('email'),query_subject=credentials.get('subject'), date = timezone.now())
        contactDetails.save()
        return HttpResponse('OK')
    return render(req,'contact.html')

def blog_single(req):
    return render(req,'blog-single.html')

def category(req,id):
    posted_blogs = Blog.objects.filter(blog_category__category_url=id,blog_status='p').order_by('-blog_date')
    blogs = []
    results = paginateResults(req,posted_blogs,ResultPerPage,'blogcategoryvalue')
    for blog in results.listItem :
        blogs.append(blog)
    blogs = prettyFilter(blogs)
    return render(req,'blog.html',{'blogs' : blogs, 'pages': range(results.pages), 'p':  results.p })

def signUp(req):
    if req.method == 'POST':
        try:
            body = req.POST
            fname = body['firstName']
            lname = body['lastName']
            username = body['username']
            email = body['email']
            password1 = body['password1']
            password2 = body['password2']
            isUserExists = User.objects.filter(username=username).exists()
            isEmailExists = User.objects.filter(email=email).exists()
            if username.isalnum() and not isUserExists and not isEmailExists and isEmail(email) and password1 == password2 :
                user = User.objects.create_user(username,email,password1)
                user.first_name = fname
                user.last_name = lname
                user.save()
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
            return HttpResponse(status=500)
        return HttpResponse('OK')
    return render(req,'signup.html')

def loginUser(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(req,user)
            return redirect( req.POST.get('redirect') or req.META.get('HTTP_REFERER') or '/')
        else: return HttpResponseBadRequest('Incorrect Credentials')
    return render(req,'login.html') if not req.user.is_authenticated else redirect('/') 

def logoutUser(req):
    logout(req)
    return redirect(req.META.get('HTTP_REFERER') or '/')

def search(req):
    qString = req.GET.get('q')
    results = []
    if qString != None and len(qString) != 0:
        result = Blog.objects.filter(blog_title__icontains=qString).order_by('-blog_date')
        results = [ item  for item in result]
        result = Blog.objects.filter(blog_content__icontains=qString).order_by('-blog_date')
        results.extend([item for item in result if item not in results])
        results = paginateResults(req,results or [],ResultPerPage,'blogsearch')
        return render(req, 'search.html', {'qs': qString or '' , 'blogs': prettyFilter(results.listItem), 'pages':range(results.pages), 'p': results.p })
    return render(req,'search.html',{})

@csrf_exempt
def uploadImage(request):
    if request.method == 'POST' and request.user.is_authenticated: # and str(request.headers['Origin']).split(':')[0] in ALLOWED_HOSTS:
        try:
            file = request.FILES.get('file') or request.FILES.get('image')
            product = Images.objects.create(image=file)
            product.save()
            return JsonResponse({'location': '/media/' + str(product.image)})
        except KeyError:
            return HttpResponseBadRequest("File not found")
        except:
            return HttpResponse("Internal server error", status=500)
    if request.user.is_authenticated:
        return render(request,'s.html') 
    else:  raise Http404("Page not found")

def postComment(req):
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