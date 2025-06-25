from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .apps import LmsConfig
from .views import CourseSubscribeAPIView, CourseViewSet, LessonViewSet

app_name = LmsConfig.name


router = SimpleRouter()
router.register("courses", CourseViewSet)
router.register("lessons", LessonViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "courses/subscribe/", CourseSubscribeAPIView.as_view(), name="course-subscribe"
    ),
]
