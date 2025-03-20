from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.db.models.signals import post_save
from videoflix_app.models import Video
from videoflix_app.signals import video_post_save
from user_auth_app.signals import user_post_save
from users_app.models import CustomUser


class VideoTests(APITestCase):
    
    def setUp(self):
        post_save.disconnect(video_post_save, sender=Video)
        post_save.disconnect(user_post_save, sender=CustomUser)
        
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@user.de', password='test123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.video = Video.objects.create(
            title = 'Testvideo',
            description = 'Testbeschreibung',
            genres = ['neu', 'test'],
            thumbnail = 'test_thumbnail.png',
            video_file = 'test_video.mp4',
        )


    def tearDown(self):
        post_save.connect(video_post_save, sender=Video)
        post_save.connect(user_post_save, sender=CustomUser)


    def test_list_video(self):
        url = reverse('video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Video.objects.count(), 1)
        self.assertContains(response, 'video_file')


    def test_post_video(self):
        url = reverse('video-list')
        data = {'test': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
