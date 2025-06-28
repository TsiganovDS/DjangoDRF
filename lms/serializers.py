from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import youtube_only_validator


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(
        validators=[youtube_only_validator], required=False, allow_blank=True
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "title",
            "preview_image",
            "description",
            "is_subscribed",
            "lesson_count",
        ]

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024)


class PriceSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default="rub")
