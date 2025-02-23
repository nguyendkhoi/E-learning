from django.contrib import admin
from .models import Question, Quiz, Result, Answer
# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Result)
admin.site.register(Quiz)
admin.site.register(Answer)
