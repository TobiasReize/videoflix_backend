from rest_framework.generics import ListAPIView
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings
from ..models import Video
from .serializers import VideoListSerializer
from shared.permission import IsAuthenticated


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class VideoListView(ListAPIView):
    """
    Shows all video instances in a list, only for authenticated users.
    """
    queryset = Video.objects.all()
    serializer_class = VideoListSerializer
    permission_classes = [IsAuthenticated]
