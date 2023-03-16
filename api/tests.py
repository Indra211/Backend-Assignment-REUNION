from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Post,User
from django.urls import reverse


class PostCreationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_post_creation_successful(self):
        url = reverse('posts')
        data = {
            "title": "Test Title",
            "description": "Test Description"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Title')
        self.assertEqual(Post.objects.get().description, 'Test Description')
        
    def test_post_creation_missing_title(self):
        url = reverse('posts')
        data = {
            "description": "Test Description"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

