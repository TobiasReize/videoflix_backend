from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from videoflix_app.models import Video
from videoflix_app.tasks import convert_120p, convert_360p, convert_720p, convert_1080p
from users_app.models import CustomUser
from user_auth_app.tasks import send_confirmation_email


class VideoTests(APITestCase):
    
    def setUp(self):
        self.get_queue_patcher = patch('django_rq.get_queue')
        self.mocked_get_queue = self.get_queue_patcher.start()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='test@user.de', email='test@user.de', password='test123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

        self.video = Video.objects.create(
            title = 'Testvideo',
            description = 'Testbeschreibung',
            genres = ['neu', 'test'],
            thumbnail = 'test_thumbnail.png',
            video_file = 'test_video.mp4',
        )

        queue = self.mocked_get_queue.return_value
        queue.enqueue.assert_any_call(send_confirmation_email, self.user.username, self.user.email, self.user.auth_token.key)
        queue.enqueue.assert_any_call(convert_120p, self.video.video_file.path)
        queue.enqueue.assert_any_call(convert_360p, self.video.video_file.path)
        queue.enqueue.assert_any_call(convert_720p, self.video.video_file.path)
        queue.enqueue.assert_any_call(convert_1080p, self.video.video_file.path)
        self.assertEqual(queue.enqueue.call_count, 5)


    def tearDown(self):
        self.get_queue_patcher.stop()


    def test_list_video(self):
        url = reverse('video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Video.objects.count(), 1)
        self.assertContains(response, 'video_file_url')


    def test_post_video_fail(self):
        url = reverse('video-list')
        data = {'test': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
