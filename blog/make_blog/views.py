from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Blog, ContactClass
from django.utils import timezone

# Create your views here.
from django.shortcuts import render

def index(req):
    return render(req,'index.html')

def blog(req):
    posted_blogs = Blog.objects.filter(blog_status='p').order_by('-blog_date')
    blogs = []
    for blog in posted_blogs[:6] :
        blogs.append(blog)
    return render(req,'blog.html')

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

