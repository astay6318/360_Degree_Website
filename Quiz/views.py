from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Subject, Quiz, Question, Option


@csrf_exempt
def create_quiz(request):
    if request.method == "POST":
        # Parse incoming JSON data
        data = json.loads(request.body)

        # Extract relevant information from the JSON data
        quiz_title = data.get("title")
        subject_name = data.get("subject")
        questions_data = data.get("questions")

        # Retrieve or create the Subject object
        subject, _ = Subject.objects.get_or_create(name=subject_name)

        # Create the Quiz object
        quiz = Quiz.objects.create(title=quiz_title, subject=subject)

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
    # Get the subject and title from the query parameters
    subject_name = request.GET.get("subject")
    quiz_title = request.GET.get("title")

    # Retrieve the Subject object
    try:
        subject = Subject.objects.get(name=subject_name)
    except Subject.DoesNotExist:
        return JsonResponse(
            {"error": f'Subject "{subject_name}" not found'}, status=404
        )

    # Retrieve the Quiz object
    try:
        quiz = Quiz.objects.get(title=quiz_title, subject=subject)
    except Quiz.DoesNotExist:
        return JsonResponse(
            {"error": f'Quiz "{quiz_title}" for subject "{subject_name}" not found'},
            status=404,
        )

    # Prepare the quiz data to be returned in the response
    quiz_data = {
        "title": quiz.title,
        "subject": quiz.subject.name,
        "questions": [
            {
                "text": question.text,
                "options": [
                    {"text": option.text, "is_correct": option.is_correct}
                    for option in question.options.all()
                ],
            }
            for question in quiz.questions.all()
        ],
    }

    # Return the quiz data in JSON format
    return JsonResponse(quiz_data)


@csrf_exempt
def get_quiz_by_title(request):
    if request.method == "GET":
        title = request.GET.get("title")
        try:
            quiz = Quiz.objects.get(title=title)
            quiz_data = {
                "title": quiz.title,
                "subject": quiz.subject.name,
                "questions": [
                    {
                        "text": question.text,
                        "options": [
                            {"text": option.text, "is_correct": option.is_correct}
                            for option in question.options.all()  # Access related options directly
                        ],
                    }
                    for question in quiz.questions.all()
                ],
            }
            return JsonResponse(quiz_data)
        except Quiz.DoesNotExist:
            return JsonResponse({"error": "Quiz not found"}, status=404)
