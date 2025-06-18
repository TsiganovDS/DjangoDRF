from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .apps import LmsConfig
from .views import CourseViewSet, LessonDetail, LessonList

app_name = LmsConfig.name


router = SimpleRouter()
router.register("courses", CourseViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonList.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetail.as_view(), name="lesson-detail"),
]
