from django.http import HttpResponseForbidden

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_teacher() or not request.user.is_authenticated:
            return HttpResponseForbidden("Not allow to access for student")
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student():
            return HttpResponseForbidden("Not allow to access for teacher")
        return view_func(request, *args, **kwargs)
    return wrapper