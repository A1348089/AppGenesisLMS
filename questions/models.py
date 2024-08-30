from django.db import models

# Create your models here.

class Questions(models.Model):
    
    QUESTION_LEVEL_CHOICES = [
        ("E", "EASY"),
        ("M", "MEDIUM"),
        ("H", "HARD"),
    ]
    title = models.CharField(max_length=50)
    topic = models.CharField(max_length=100, default=None)
    short_description = models.CharField(max_length=200, default=None)
    long_description = models.CharField(max_length=300, default=None)
    leve = models.CharField(max_length=1, choices=QUESTION_LEVEL_CHOICES, default="E")
    question = models.CharField(max_length=500, null=False)
    answer = models.JSONField(null=False)

    def __str__(self):
        return self.question
