from django.contrib.auth import get_user_model
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return super().__str__()


class Enrollment(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
