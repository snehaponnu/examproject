
# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    ans1 = models.CharField(max_length=255)
    ans2 = models.CharField(max_length=255)
    ans3 = models.CharField(max_length=255)
    ans4 = models.CharField(max_length=255)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Exam, on_delete=models.CASCADE)
    answer_id = models.PositiveIntegerField()  # Store the selected answer (1, 2, 3, or 4)


