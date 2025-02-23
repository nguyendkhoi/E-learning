
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addcourse", views.add_course, name="addcourse"),
    path("course/<int:course_id>", views.course_detail, name="course_detail"),
    path("course/<int:course_id>/remove", views.remove_course_view, name="remove_course_view"),
    path("course/<int:course_id>/addlecture", views.add_lecture, name="addlecture"),
    path("course/lecture/<int:lecture_id>", views.lecture_views, name="lecture_views"),
    path("course/lecture/<int:lecture_id>/remove", views.remove_lecture, name="remove_lecture"),
    path("course/<int:course_id>/enroll/", views.enroll_course, name="enroll_course"),
    path("mycourse", views.my_course, name="my_course"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("student_tests/<int:student_id>", views.student_tests, name="student_tests"),
    path("people", views.people, name="people"),
    
    path("course/<int:lecture_id>/addquiz/", include('quizes.urls', namespace='quizes')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

