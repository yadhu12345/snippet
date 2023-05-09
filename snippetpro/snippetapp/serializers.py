from rest_framework import serializers
from .models import Snippet, Tag

class LTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class LSnippetSerializer(serializers.ModelSerializer):
    tag = LTagSerializer()

    class Meta:
        model = Snippet
        fields = '__all__'
        
class DSnippetSerializer(serializers.ModelSerializer):
    tag = LTagSerializer()

    class Meta:
        model = Snippet
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')

class SnippetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        tags = []
        for tag_data in tags_data:
            title = tag_data['title']
            tag, created = Tag.objects.get_or_create(title=title)
            tags.append(tag)
        print(validated_data)
        snippet = Snippet.objects.create(**validated_data)
        print("#################################")
        print(snippet)
        snippet.tags.set(tags)
        return snippet

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'content', 'tags')
        extra_kwargs = {
            'tags': {'required': True}  # set required=True to ensure tags are always provided
        }