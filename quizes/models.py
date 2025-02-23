import random
from django.db import models
from final_project.models import User, Lecture
# Create your models here.

DIFF_CHOICES = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),

)

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    number_of_question = models.IntegerField(default=1)
    required_score_to_pass = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFF_CHOICES)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name="quiz_of_lecture")
    
    def __str__(self):
        return f"quiz: {self.name}"
    
    def get_questions(self):
        questions = list(self.question.all())
        random.shuffle(questions)
        return questions

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="question")

    def __str__(self):
        return f"{self.text}"
    
    def get_answer(self):
        answers = list(self.answer.all())
        random.shuffle(answers)
        return answers

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer")

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"
    
class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_result")
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)