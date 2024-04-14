from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Lesson, Quiz, Question, Option


@csrf_exempt
def create_quiz(request):
    if request.method == "POST":
        # Parse incoming JSON data
        data = json.loads(request.body)

        # Extract relevant information from the JSON data
        quiz_title = data.get("title")
        lesson_id = data.get("lesson_id")
        questions_data = data.get("questions")

        # Retrieve or create the Lesson object
        lesson, _ = Lesson.objects.get_or_create(lesson_id=lesson_id)

        # Check if a quiz already exists for the lesson
        try:
            quiz = Quiz.objects.get(lesson=lesson)
        except Quiz.DoesNotExist:
            # Create a new quiz object for the lesson
            quiz = Quiz.objects.create(title=quiz_title, lesson=lesson)

        # Create Question and Option objects and associate them with the Quiz
        for question_data in questions_data:
            question_text = question_data.get("text")
            question = Question.objects.create(text=question_text, quiz=quiz)
            for option_data in question_data.get("options", []):
                option_text = option_data.get("text")
                is_correct = option_data.get("is_correct", False)
                Option.objects.create(
                    text=option_text, question=question, is_correct=is_correct
                )

        # Return a JSON response indicating success
        return JsonResponse({"message": "Quiz created successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_quiz(request):
    if request.method == "GET":
        lesson_id = request.GET.get("lesson_id")

        # Retrieve the Lesson object
        try:
            # print(lesson_id == "c222a68d-5dc6-4647-aceb-ede3dde31c54")
            lesson = Lesson.objects.get(lesson_id=lesson_id)
        except Lesson.DoesNotExist:
            return JsonResponse(
                {"error": f'Lesson with ID "{lesson_id}" not found'}, status=404
            )

        # Retrieve the Quiz object associated with the Lesson
        try:
            quiz = Quiz.objects.get(lesson=lesson)
        except Quiz.DoesNotExist:
            return JsonResponse(
                {"error": f'Quiz for Lesson with ID "{lesson_id}" not found'},
                status=404,
            )

        # Retrieve all questions and options associated with the Quiz
        questions = quiz.questions.all()
        quiz_data = {
            "title": quiz.title,
            "lesson_id": lesson.lesson_id,
            "questions": [
                {
                    "text": question.text,
                    "options": [
                        {"text": option.text, "is_correct": option.is_correct}
                        for option in question.options.all()
                    ],
                }
                for question in questions
            ],
        }

        # Return the quiz data in JSON format
        return JsonResponse(quiz_data)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
