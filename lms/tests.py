from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Lesson


class LessonCRUDAndSubscriptionTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create(email="owner@example.com", password="pass123")
        self.user = User.objects.create(email="user@example.com", password="pass123")
        self.moder = User.objects.create(email="moder@example.com", password="pass123")
        self.course = Course.objects.create(title="Тестовый курс", owner=self.owner)
        self.lesson = Lesson.objects.create(
            title="Тестовый урок", course=self.course, owner=self.owner
        )

    def generate_image(self):
        return SimpleUploadedFile(
            "test.gif",
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00"
            b"\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c"
            b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
            content_type="image/gif",
        )

    def test_owner_can_create_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lms:lesson-list")
        data = {
            "title": "Новый урок",
            "course": self.course.id,
            "description": "Описание урока",
            "preview_image": self.generate_image(),
            "video_link": "https://youtube.com/test",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_owner_can_update_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lms:lesson-detail", args=[self.lesson.id])
        data = {
            "title": "Попытка модера",
            "description": "Описание от модера",
            "preview_image": self.generate_image(),
            "video_link": "https://youtube.com/test",
            "course": self.course.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Попытка модера")

    def test_anon_can_not_delete_lesson(self):
        url = reverse("lms:lesson-detail", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_delete_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lms:lesson-detail", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_un_authenticated_can_not_subscribe(self):
        url = reverse("lms:course-subscribe")
        data = {
            "title": "Попытка модера",
            "description": "Описание от модера",
            "preview_image": self.generate_image(),
            "video_link": "https://youtube.com/test",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
