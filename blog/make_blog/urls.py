from django.urls import path
from .views import *

urlpatterns = [
    path('', index,name='blogindex'),
    path('blog/', blog,name='blogvalue'),
    path('blog/<str:id>', blogpost,name='blogpostvalue'),
    path('logout', logoutUser,name='blogLogout'),
    path('login', loginUser,name='blogLogin'),
    path('signup', signUp,name='userSignUp'),
    path('profile', userProfile,name='userProfile'),
    path('search', search,name='blogsearch'),
    path('reset-password', resetPassword,name='resetPassword'),
    path('post-comment', postComment,name='postComment'),
    path('upload-image', uploadImage,name='upload_image'),
    path('category/<str:id>', category,name='blogcategoryvalue'),
    path('features/', features,name='blogfeatures'),
    path('pricing/', pricing,name='blogpricing'),
    path('contact/', contact,name='blogcontact'),
    path('blog-single/', blog_single,name='blog-single'),
]