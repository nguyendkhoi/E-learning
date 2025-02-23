from django.db import IntegrityError
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User, Course, Lecture
from django.contrib.auth.password_validation import validate_password
from .decorators import teacher_required, student_required
from quizes.models import Quiz, Result

def index(request):
    if request.user.is_authenticated:
        if request.user.role == "teacher":
            courses = Course.objects.filter(owner=request.user).all()
            return render(request, "project/index.html", {
                "courses": courses,
            })
        elif request.user.role == "student":
            courses = Course.objects.all()
            return render(request, "project/index.html", {
                "courses": courses,
            })
    
    return render(request, "project/index.html", {
        "message": "You must login before see any course",
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print("user:", user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "project/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "project/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        full_name = request.POST["full_name"]
        passwd = request.POST["password"]
        confirmpass = request.POST["confirmation"]
        role = request.POST.get('role', 'student')
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, "project/register.html", {
                "message": "Email is already in use!"
            })
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "project/register.html", {
                "message": "Username already taken!"
            })
        
        # Check if password is the same as confirmpassword
        if passwd != confirmpass:
            return render(request, "project/register.html", {
                "message": "Passwords must match!"
            })
        try:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=passwd, 
                full_name=full_name,
                role=role
            )
            print("registrer successful")
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        except IntegrityError:
            return render(request, "project/register.html", {
                "message": "Error can't registrer"
            })
    
    return render(request, "project/register.html")

@teacher_required
def add_course(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"].replace("_", " ").title()
        owner = request.user
        if Course.objects.filter(owner=owner, title=title).exists():
            return render(request, "project/addCourse.html", {
                "message": "You are already use this title"
            })
        
        if not all([title, description, category]):
            return render(request, "project/addCourse.html", {
                "message": "All fields are required"
            })
        
        Course.objects.create(title=title, description=description, category=category, owner=owner)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "project/addCourse.html")

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user.role == "teacher":
        return render(request, "project/course_detail.html", {
            "course": course,
            "is_owner": course.owner == request.user,
        })
    else:
        return render(request, "project/course_detail_student.html", {
            "course": course,
            "is_owner": False,
        })

def remove_course_view(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == "POST" and request.user == course.owner:
        course.delete()
    return HttpResponseRedirect(reverse("index"))

def add_lecture(request, course_id):
    if request.method == "POST":
        course = Course.objects.get(id=course_id)
        title = request.POST["title"]
        description = request.POST["description"]
        content = request.POST["content"]

        if 'video_file' in request.FILES:
            video_file = request.FILES['video_file']
        else:
            video_file = None

        Lecture.objects.create(
            courses=course,
            title=title,
            description=description,
            content=content,
            video_file=video_file
        )
    return HttpResponseRedirect(reverse("course_detail", kwargs={'course_id': course_id}))


def lecture_views(request, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    quizes = lecture.get_all_quizzes()
    print(" quizes: ", quizes)
    quizes_data = []
    for quiz in quizes:
        passed = False
        result = Result.objects.filter(user=request.user, quiz=quiz).order_by('-score').first()
        if result:
            print("result:", result)
            print("quiz.required_score_to_pass: ", quiz.required_score_to_pass)
            print("result score: ", result.score)
            passed = result.score >= quiz.required_score_to_pass
        quizes_data.append({
            "quiz": quiz,
            "passed": passed
        })
        print ("quizes_data: ", quizes_data)
    return render(request, 'project/lecture.html', {
        'lecture': lecture,
        'is_owner': lecture.courses.owner == request.user,
        'quizes': quizes_data,
    })
    
def remove_lecture(request, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    course_id = lecture.courses.id
    if request.method == "POST" and lecture.courses.owner == request.user:
        lecture.delete()

    return HttpResponseRedirect(reverse("course_detail", kwargs={'course_id': course_id}))

def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user in course.students.all():
        return HttpResponseRedirect(reverse("course_detail", kwargs={'course_id': course_id}))

    course.students.add(request.user)
    course.save()
    
    return HttpResponseRedirect(reverse("course_detail", kwargs={'course_id': course_id}))

@student_required
def my_course(request):
    courses = Course.objects.filter(students=request.user)
    return render(request, 'project/index.html', {
        'courses': courses
    })

def profile(request, user_id):
    print("hi")
    user = get_object_or_404(User, id=user_id)
    nb = 0
    teacher_of_student = False
    if (user.role == "teacher"):
        courses = Course.objects.filter(owner=user)
        for course in courses:
            nb += course.students.count()
    else:
        courses = Course.objects.filter(students=user)
        #if request user is the user so he can see his score
        if (user == request.user):
            teacher_of_student = True
        
        else:
            courses = Course.objects.filter(students=user)
            #check if the request user is the teacher of the student
            for course in courses:
                if course.owner == request.user:
                    teacher_of_student = True
                    break

    return render(request, 'project/profile.html',
        {
            "user": user,
            "nb_students": nb,
            "teacher_of_student": teacher_of_student
        })


def student_tests(request, student_id):
    student = get_object_or_404(User, id=student_id)

    if student == request.user:
        courses = Course.objects.filter(students=student).prefetch_related(
        'lectures',
        'lectures__quiz_of_lecture'
    )
    else:
        courses = Course.objects.filter(students=student, owner=request.user).prefetch_related(
            'lectures',
            'lectures__quiz_of_lecture'
        )
    
    courses_data = []

    for course in courses:
        course_data = {
            "course": {
                "title": course.title,
            },
            "lectures": []
        }

        for lecture in course.lectures.all():
            lecture_data = {
                "title": lecture.title,
                "quizes": []
            }

            for quiz in lecture.quiz_of_lecture.all():
                result = Result.objects.filter(user=student, quiz=quiz).order_by('-score').first()
                if(not result):
                    quiz_data = {
                    "title": quiz.name,
                    "score": "Not done yet",
                    }
                else:
                    quiz_data = {
                        "title": quiz.name,
                        "score": result.score,
                    }
                lecture_data["quizes"].append(quiz_data)

            course_data["lectures"].append(lecture_data)

        courses_data.append(course_data)
    print("courses: ", courses_data)
    return JsonResponse({"courses": courses_data})

def people(request):
    user = User.objects.get(id=request.user.id)
    courses_data = []

    if user.role == "teacher":
        courses = Course.objects.filter(owner=user)
        get_peoples = lambda course: course.students.all()
    else:
        courses = Course.objects.filter(students=user)
        get_peoples = lambda course: [course.owner]

    for course in courses:
        course_dict = {
            "course": {"title": course.title},
            "peoples": []
        }
        
        for person in get_peoples(course):
            person_data = {
                "fullname": person.full_name,
                "id": person.id
            }
            course_dict["peoples"].append(person_data)
        
        courses_data.append(course_dict)

    return render(request, "project/people.html", {
        "courses": courses_data
    })