from rest_framework import serializers
from News.models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id","title", "image", "content"]
