from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModeratorReadOnly

from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsModeratorReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Course.objects.all()
        if user.groups.filter(name="Модераторы").exists():
            return queryset
        return queryset.filter(owner=user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsModeratorReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Lesson.objects.all()
        if user.groups.filter(name="Модераторы").exists():
            return queryset
        return queryset.filter(owner=user)


class CourseSubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
