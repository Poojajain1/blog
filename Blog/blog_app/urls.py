from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('show/<int:blog_id>/', show_blog),
    path('show/', show_blog),
    path('blog-view/', ShowBlogAPIView.as_view()),
    path('list-view/', ShowUsersAPIView.as_view()),


]
