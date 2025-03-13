from rest_framework.generics import ListAPIView
from ..models import Video
from .serializers import VideoListSerializer


class VideoListView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoListSerializer
