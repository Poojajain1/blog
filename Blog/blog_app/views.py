from django.shortcuts import render
#from django.views import generic
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import Blogserializer, UserSerializer
from .models import BlogModel
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
import json
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
# Create your views here.
# @csrf_exempt


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def show_blog(request, blog_id=None):
    if request.method == "GET":
        blogs = BlogModel.objects.all()
        blog_serializer = Blogserializer(blogs, many=True)
        return Response(blog_serializer.data)

    if request.method == "POST":
        data = JSONParser().parse(request)
        title = data['title']
        content = data['content']

        blog = BlogModel.objects.create(
            title=title, content=content, created_by=request.user)

        return Response({'message': 'Blog created successfully.'})
        #user_blog= BlogModel.objects.get(title=data['title'])
        # if user_blog:
        # return Response({"message":"data duplicate - was not inserted"})

        # blog_serializer = Blogserializer(data=data)
        # if blog_serializer.is_valid():
        #     blog_serializer.save()
        # else:
        #     return Response({"message": "data invalid - was not inserted"})
        # return Response({"message": "data inserted"})

    if request.method == "PUT":
        blog = BlogModel.objects.get(blog_id=blog_id)
        data = JSONParser().parse(request)
        blog_serializer = Blogserializer(blog, data=data)
        if blog_serializer.is_valid():
            blog_serializer.save()
        else:
            return Response({"message": "data invalid - was not inserted"})
        return Response({"message": "data Updated"})

    if request.method == "DELETE":
        try:
            blog = BlogModel.objects.get(blog_id=blog_id)
            blog.delete()
        except:
            return Response({"message": "data not Deleted, no blog id there"})
        return Response({"message": "data Deleted"})


class ShowUsersAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ShowBlogAPIView(ListAPIView):
    queryset = BlogModel.objects.all()
    serializer_class = Blogserializer


class Signup(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']

        if len(username) > 6:
            messages.error(
                request, " Username must contain letters,numbers and less than 10 chars.")

        if password1 != password2:
            messages.error(
                request, " Passwords should match.")

        user = User.objects.create_user(username, email, password1)
        token = RefreshToken.for_user(user)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return Response({'username': username, 'Jwt_refresh_token': str(token),
                         'Jwt_access_token': str(token.access_token), })


class Login(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = JSONParser().parse(request)
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, " Successfully Logged In.")
            return Response({"meassage": " Successfully Logged In."})
        else:
            messages.error(
                request, " Invalid credintials, Please try again.")
            return Response({"meassage": " Invalid Crediantials."})


@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    messages.error(request, "Successfully Logout.")


# @api_view(['POST'])
# def login(request):
   # data = JSONParser().parse(request)
    #username = data['username']
    #password = data['password']
    #user = User.objects.get(username=username)

    # if user.check_password(password):
    #token_obj, created = Token.objects.get_or_create(user=user)
    # return Response({"message":"Login successsful","token":token_obj.key})
    # return Response({"message":"Login unsuccesssful"})
