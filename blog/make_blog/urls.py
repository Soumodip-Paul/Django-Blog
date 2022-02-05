from django.urls import path
from .views import *
from . import payments

urlpatterns = [
    path('', index,name='blogindex'),
    path('activate/<str:id>/<token>', activate, name="activate"),
    path('blog/', blog,name='blogvalue'),
    path('blog/<str:id>', blogpost,name='blogpostvalue'),
    path('blog-single/', blog_single,name='blog-single'),
    path('category/<str:id>', category,name='blogcategoryvalue'),
    path('contact/', contact,name='blogcontact'),
    path('course', courses,name='blogcourses'),
    path('email-reset-password', sendPasswordResetLink,name='resetPasswordsendLink'),
    path('features/', features,name='blogfeatures'),
    path('features/<str:page>', featuresPage,name='blogfeaturesPage'),
    path('favicon.ico', favicon,name='favicon'),
    path('login', loginUser,name='blogLogin'),
    path('logout', logoutUser,name='blogLogout'),
    path('post-comment', postComment,name='postComment'),
    path('pricing', payments.startPayment,name='blogpricing'),
    path('privacy', privacy,name='privacy_policy'),
    path('profile', userProfile,name='userProfile'),
    path('payment/', payments.validate,name='payment'),
    path('rating', userRating,name='rate_us'),
    path('reset-email', sendEmailResetLink,name='resetEmailSendLink'),
    path('reset-email/<str:uid>/<str:email>/<str:token>', resetEmailLink,name='reset-email'),
    path('reset-password', resetPassword,name='resetPassword'),
    path('reset-password/<str:uid>/<str:token>', resetPasswordLink,name='reset-password'),
    path('signup', signUp,name='userSignUp'),
    path('search', search,name='blogsearch'),
    path('terms-and-condition', terms,name='terms_and_condition'),
    path('upload-image', uploadImage,name='upload_image'),
]