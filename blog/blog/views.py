from django.shortcuts import render

def index(req):
    return render(req,'index.html')

def blog(req):
    return render(req,'blog.html')

def features(req):
    return render(req,'features.html')

def pricing(req):
    return render(req,'pricing.html')

def contact(req):
    return render(req,'contact.html')

def blog_single(req):
    return render(req,'blog-single.html')
