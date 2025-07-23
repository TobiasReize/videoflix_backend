from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.conf import settings
from ..models import Video
from .serializers import VideoListSerializer


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoListView(ListAPIView):
    """
    Shows all video instances in a list, only for authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cache_key = f"video_list_user_{request.user.id}"
        data = cache.get(cache_key)
        
        if data is None:
            videos = Video.objects.all()
            serializer = VideoListSerializer(videos, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=CACHE_TTL)

        return Response(data)
