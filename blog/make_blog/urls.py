from django.urls import path
from .views import *

urlpatterns = [
    path('', index,name='blogindex'),
    path('activate/<str:id>', activate, name="activate"),
    path('blog/', blog,name='blogvalue'),
    path('blog/<str:id>', blogpost,name='blogpostvalue'),
    path('blog-single/', blog_single,name='blog-single'),
    path('category/<str:id>', category,name='blogcategoryvalue'),
    path('contact/', contact,name='blogcontact'),
    path('features/', features,name='blogfeatures'),
    path('login', loginUser,name='blogLogin'),
    path('logout', logoutUser,name='blogLogout'),
    path('post-comment', postComment,name='postComment'),
    path('pricing/', pricing,name='blogpricing'),
    path('profile', userProfile,name='userProfile'),
    path('reset-password', resetPassword,name='resetPassword'),
    path('signup', signUp,name='userSignUp'),
    path('search', search,name='blogsearch'),
    path('upload-image', uploadImage,name='upload_image'),
    path('update-email',updateEmail,name='updateEmail'),
]