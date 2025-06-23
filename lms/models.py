from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview_image = models.ImageField(upload_to="course_previews/")
    description = models.TextField()
    users = models.ManyToManyField(User, related_name="courses")
    owner = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="owned_courses"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to="lesson_previews/")
    video_link = models.URLField()
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="owned_lessons"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
