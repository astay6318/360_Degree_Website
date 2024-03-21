from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "Quiz"


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        app_label = "Quiz"


class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE,default=1)

    class Meta:
        app_label = "Quiz"


class Option(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question,
        related_name="options",
        on_delete=models.CASCADE,
        default=1  # Provide a suitable default value here
    )
    is_correct = models.BooleanField(default=False)

    class Meta:
        app_label = "Quiz"

