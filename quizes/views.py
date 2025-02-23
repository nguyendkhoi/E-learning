from django.shortcuts import render
from .models import Quiz, Question, Answer, Result
from final_project.models import Lecture
from django.http import HttpResponseNotFound, JsonResponse
import json

def create_quiz(request, lecture_id):
    if request.method == 'POST':
        lecture = Lecture.objects.get(id=lecture_id)
        name = request.POST["name"]
        number_of_question = request.POST["number_of_question"]
        difficulty = request.POST["difficulty"]
        percentage = request.POST["percentage"]
        print (f"lectuer: {lecture}, name: {name}, number: {number_of_question}, difficulty: {difficulty}, percentage: {percentage}")
        # Check all field
        if not name or not number_of_question or not difficulty:
            return JsonResponse({
                "error": "All fields are required"
            }, status=400)
        
        quiz = Quiz.objects.create(
            name=name,
            number_of_question=number_of_question,
            difficulty=difficulty,
            lecture=lecture,
            required_score_to_pass=percentage
        )
        return JsonResponse({
            "message": "Create new quize succesfully",
            "number_of_question": number_of_question,
            "quiz_id": quiz.id,
            "lecture_id": lecture_id
        })

def save_question_answer(request, quiz_id, lecture_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_text = data.get('question_text')
            answers = data.get('answers', [])
            # Get the quiz instance
            quiz = Quiz.objects.get(id=quiz_id)
            
            # Create question
            question = Question.objects.create(
                text=question_text,
                quiz=quiz
            )
            
            # Create answers for the question
            for answer in answers:
                Answer.objects.create(
                    text=answer['text'],
                    correct=answer['correct'],
                    question=question
                )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Question and answers saved successfully',
                'question_id': question.id,
                'quiz_id': quiz_id,
         })
        except Quiz.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Quiz not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({
        'status': 'error',
        'error': 'Invalid request method'
    }, status=400)

def quiz_view(request, lecture_id, quiz_id):
    if request.method == "GET":
        try:
            lecture = Lecture.objects.get(id=lecture_id)
            quiz = Quiz.objects.get(lecture=lecture, id=quiz_id)
            questions_quiz = quiz.get_questions()
            print (f"lectureID: ", lecture_id)
            return render(request, 'quiz/quize.html', {
                'quiz': quiz,
                'questions': questions_quiz,
                'quiz_id': quiz_id,
                'lecture_id': lecture_id,
            })
            
        except Quiz.DoesNotExist:
            return HttpResponseNotFound("Quiz not found")
            

def save_quiz(request, quiz_id):
    data = json.loads(request.body)

    questions = []
    for k in data.keys():
        try:
            question = Question.objects.get(text=k)
            questions.append(question)
        except Question.DoesNotExist:
            print(f"Warning: Question with text '{k}' not found.")
            return JsonResponse({'error': f'Question with text "{k}" not found.'}, status=400)

    user = request.user
    quiz = Quiz.objects.get(id=quiz_id)

    score = 0
    multiplier = 100 / quiz.number_of_question
    results = []
    correct_answer = None

    for q in questions:
        a_selected = data[q.text]

        if a_selected != "":
            question_answers = Answer.objects.filter(question=q)
            for a in question_answers:
                if a_selected == a.text:
                    if a.correct:
                        score += 1
                        correct_answer = a.text
                else:
                    if a.correct:
                        correct_answer = a.text
            results.append({str(q): {'correct_answer': correct_answer,
                                     'answered': a_selected}})
        else:
            results.append({str(q): 'not answered'})

    score_ = score * multiplier
    print("score:", score_)
    Result.objects.create(quiz=quiz, user=user, score=score_)

    return JsonResponse({'passed': score_ >= quiz.required_score_to_pass, 'score': score_, 'results': results})