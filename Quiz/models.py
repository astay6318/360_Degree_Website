from django.db import models


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, primary_key=True)

    class Meta:
        app_label = "Quiz"


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=None)

    class Meta:
        app_label = "Quiz"


class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(
        Quiz, related_name="questions", on_delete=models.CASCADE, default=1)

    class Meta:
        app_label = "Quiz"


class Option(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question,
        related_name="options",
        on_delete=models.CASCADE,
        default=1,  # Provide a suitable default value here
    )
    is_correct = models.BooleanField(default=False)

    class Meta:
        app_label = "Quiz"
