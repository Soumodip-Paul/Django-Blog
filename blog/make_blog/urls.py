from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.index,name='blogindex'),
    path('blog/', views.blog,name='blogvalue'),
    path('features/', views.features,name='blogfeatures'),
    path('pricing/', views.pricing,name='blogpricing'),
    path('contact/', views.contact,name='blogcontact'),
    path('blog-single/', views.blog_single,name='blog-single'),
]