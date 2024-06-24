from django.db import models


class Enrollment(models.Model):
    user_id = models.IntegerField()
    course_id = models.IntegerField()
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'course_id')
