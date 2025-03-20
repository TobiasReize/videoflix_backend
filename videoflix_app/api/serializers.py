from rest_framework import serializers
from ..models import Video


class VideoListSerializer(serializers.ModelSerializer):
    video_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'genres', 'thumbnail', 'video_file_url', 'created_at', 'updated_at']
    
    def get_video_file_url(self, obj):
        """
        Returns the relative path of the video file.
        """
        if obj.video_file:
            return obj.video_file.url
        return None
