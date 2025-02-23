from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    ROLE_CHOICES = [
         ('student', 'Student'),
         ('teacher', 'Teacher')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def is_teacher(self):
         return self.role == 'teacher'
    
    def is_student(self):
         return self.role == 'student'
    
    def __str__(self):
        return self.username

class Course(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created', limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, limit_choices_to={'role': 'student'}, related_name="courses_enrolled", blank=True)
    def __str__(self):
            return f"{self.title}"

class Lecture(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    content = models.TextField()
    video_file = models.FileField(
        upload_to='lectures/videos/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])]
    )

    def __str__(self):
        return f"{self.title}"

    def get_all_quizzes(self):
        return self.quiz_of_lecture.all()
