from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'quizes'

urlpatterns = [
    path("create/", views.create_quiz, name="create_quiz"),
    path("save-question-answer/<int:quiz_id>/", views.save_question_answer, name="save-question-answer"),
    path("<int:quiz_id>/", views.quiz_view, name="quiz_view"),
    path("<int:quiz_id>/save_quiz/", views.save_quiz, name="save_quiz")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
