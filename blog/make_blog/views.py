from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect, render
from django.utils import timezone
from bs4 import BeautifulSoup
from .models import Blog, BlogCategory, ContactClass, Images
from .utils import isEmail, pretty_date, prettyFilter

# Create your views here.
from django.shortcuts import render

def index(req):
    return render(req,'index.html')

def blog(req):
    posted_blogs = Blog.objects.filter(blog_status='p').order_by('-blog_date')
    blogs = []
    for blog in posted_blogs[:9] :
        blogs.append(blog)
    blogs = prettyFilter(blogs)
    return render(req,'blog.html',{'blogs' : blogs })
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
            blog_desc = BeautifulSoup(blogPostItem.blog_content,"html.parser").get_text()[:120]
            blogPostItem.blog_date = pretty_date(blogPostItem.blog_date)
            return render(req,'blog-post.html',{ 'blog': blogPostItem, 'blog_desc': blog_desc, 'categories': categories })
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
    for blog in posted_blogs[:9] :
        blogs.append(blog)
    blogs = prettyFilter(blogs)
    return render(req,'blog.html',{'blogs' : blogs })

def signUp(req):
    if req.method == 'POST':
        # To be implemented user auth flow
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
    print(req)
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username=username,password=password)
        print(username,password)
        if user is not None:
            login(req,user)
            return redirect(req.META['HTTP_REFERER'])
        else: return HttpResponseBadRequest('Incorrect Credentials')
    return redirect('blogindex')

def logoutUser(req):
    logout(req)
    return redirect(req.META['HTTP_REFERER'])

def search(req):
    qString = req.GET.get('q')
    results = []
    if qString != None and len(qString) != 0:
        result = Blog.objects.filter(blog_title__icontains=qString).order_by('-blog_date')
        results = [ item  for item in result]
        result = Blog.objects.filter(blog_content__icontains=qString).order_by('-blog_date')
        results.extend([item for item in result if item not in results])
        results = results[:9]
    return render(req, 'search.html', {'qs': qString or '' , 'blogs': prettyFilter(results) })

@csrf_exempt
def uploadImage(request):
    if request.method == 'POST':
        try:
            print(request.headers)
            print(request.POST)
            print(request.FILES)
            file = request.FILES['file']
            product = Images.objects.create(image=file)
            product.save()
            return JsonResponse({'location': '/media/' + str(product.image)})
        except KeyError:
            return HttpResponseBadRequest("File not found")

    return render(request,'s.html')