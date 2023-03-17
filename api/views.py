from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import User, Post, Like, Comment
from .serializers import UserSerializer, PostSerializer, LikeSerializer, CommentSerializer
from django.http import HttpResponse


def index(request):
    html = "WELCOME TO REUNION SERVICE"
    return HttpResponse(html)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

@api_view(['POST'])
def authenticate_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, id):
    user_to_follow = get_object_or_404(User, id=id)
    request.user.following.add(user_to_follow)
    return Response({'success': True})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, id):
    user_to_unfollow = get_object_or_404(User, id=id)
    request.user.following.remove(user_to_unfollow)
    return Response({'success': True})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def posts(request):
    title = request.data.get('title')
    description = request.data.get('description')
    post = Post.objects.create(title=title, description=description, author=request.user)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    post.delete()
    return Response({'success': True})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    serializer = LikeSerializer(like)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, id):
    post = get_object_or_404(Post, id=id)
    Like.objects.filter(user=request.user, post=post).delete()
    return Response({'success': True})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    comment_text = request.data.get('comment')
    comment = Comment.objects.create(text=comment_text, user=request.user, post=post)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_details(request, id):
    post = get_object_or_404(Post, id=id)
    likes = post.likes.count()
    comments = Comment.objects.filter(post=post)
    serializer = PostSerializer(post, context={'likes': likes, 'comments': comments},)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = Post.objects.all()
    serialized_posts = PostSerializer(posts,many = True)
    return Response(serialized_posts.data)
    
