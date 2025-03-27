from rest_framework import serializers
from videoflix_app.models import Video, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class VideoListSerializer(serializers.ModelSerializer):
    video_file_url = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

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
    
    def get_genres(self, obj):
        """
        Returns the names of the genres.
        """
        return [genre.name for genre in obj.genres.all()]
