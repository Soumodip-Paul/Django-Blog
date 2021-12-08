from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.index,name='blogindex'),
    path('blog/', views.blog,name='blogvalue'),
    path('blog/<str:id>', views.blogpost,name='blogpostvalue'),
    path('logout', views.logoutUser,name='blogLogout'),
    path('login', views.loginUser,name='blogLogin'),
    path('signup', views.signUp,name='userSignUp'),
    path('profile', views.userProfile,name='userProfile'),
    path('search', views.search,name='blogsearch'),
    path('post-comment', views.postComment,name='postComment'),
    path('upload-image', views.uploadImage,name='upload_image'),
    path('category/<str:id>', views.category,name='blogcategoryvalue'),
    path('features/', views.features,name='blogfeatures'),
    path('pricing/', views.pricing,name='blogpricing'),
    path('contact/', views.contact,name='blogcontact'),
    path('blog-single/', views.blog_single,name='blog-single'),
]