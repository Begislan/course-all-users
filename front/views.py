from django.http import Http404
from django.http import HttpResponseForbidden
from accounts.models import CustomUser as User, CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Lesson, Content
from functools import wraps
from django.contrib.auth.decorators import login_required

def role_required(role):
    """
    Декоратор для проверки роли пользователя.
    role: 'teacher' или 'student'
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')  # сначала проверка на авторизацию
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type == role:
                return view_func(request, *args, **kwargs)
            # если роль не совпадает → редирект или 403
            return redirect('/')
            # можно вместо redirect вернуть HttpResponseForbidden
        return _wrapped_view
    return decorator



def home(request):
    user = request.user

    if user.is_authenticated:
        if user.user_type == 'teacher':
            context = {'status': 'Преподаватель', 'url': 'courses'}
        elif user.user_type == 'student':
            context = {'status': 'Студент', 'url': 'student'}
        else:
            context = {'status': 'Неактивный пользователь', 'url': ''}
    else:
        context = {'status': 'Гость', 'url': ''}

    return render(request, 'front/home.html', context)

@role_required('teacher')
@login_required
def teacher_all(request, course_id=None, lesson_id=None):
    courses = Course.objects.filter(author=request.user)
    selected_course = get_object_or_404(Course, id=course_id, author=request.user) if course_id else None
    lessons = selected_course.lessons.all() if selected_course else None

    selected_lesson = None
    contents = None

    if lesson_id:
        # Получаем урок только если он принадлежит курсам пользователя
        try:
            selected_lesson = Lesson.objects.get(id=lesson_id, course__author=request.user)
            contents = selected_lesson.contents.all()
        except Lesson.DoesNotExist:
            raise Http404("Урок не найден или вы не имеете доступа")

    return render(request, 'teacher/teacher.html', {
        'courses': courses,
        'selected_course': selected_course,
        'lessons': lessons,
        'selected_lesson': selected_lesson,
        'contents': contents,
    })

@role_required('teacher')
@login_required
def add_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')

        if title:
            Course.objects.create(
                author=request.user,
                title=title,
                description=description,
                image=image
            )
    return redirect('courses')

@role_required('teacher')
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Проверка: пользователь — автор курса
    if course.author != request.user:
        return HttpResponseForbidden("У вас нет прав на редактирование этого курса.")

    if request.method == "POST":
        new_title = request.POST.get("title")
        if new_title:
            course.title = new_title
            course.save()
    return redirect("courses")  # или куда вы перенаправляете после обновления

@role_required('teacher')
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Проверка на автора
    if course.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот курс.")

    if request.method == "POST":
        course.delete()

    return redirect("courses")

@role_required('teacher')
@login_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id, author=request.user)
    if request.method == "POST":
        title = request.POST.get('title')
        order = request.POST.get('order', 0)
        if title:
            Lesson.objects.create(course=course, title=title, order=order)
    return redirect('course_detail', course_id=course.id)

@role_required('teacher')
@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course__author=request.user)
    if request.method == "POST":
        title = request.POST.get('title')
        order = request.POST.get('order', 0)
        if title:
            lesson.title = title
            lesson.order = order
            lesson.save()
    return redirect('course_detail', course_id=lesson.course.id)

@role_required('teacher')
@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course__author=request.user)
    course_id = lesson.course.id
    lesson.delete()
    return redirect('course_detail', course_id=course_id)

@role_required('teacher')
@login_required
def add_content(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        content_data = request.POST.get('content_data')
        file = request.FILES.get('file')
        order = request.POST.get('order') or 0

        Content.objects.create(
            lesson=lesson,
            content_type=content_type,
            content_data=content_data if content_type != 'file' else '',
            file=file if content_type == 'file' else None,
            order=order
        )
        return redirect('lesson_detail', course_id=lesson.course.id, lesson_id=lesson.id)

@role_required('teacher')
@login_required
def edit_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    if request.method == 'POST':
        content.content_type = request.POST.get('content_type')
        content.content_data = request.POST.get('content_data')
        content.order = request.POST.get('order') or 0
        content.save()
        return redirect('lesson_detail', course_id=content.lesson.course.id, lesson_id=content.lesson.id)

@role_required('teacher')
@login_required
def delete_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    lesson = content.lesson
    content.delete()
    return redirect('lesson_detail', course_id=lesson.course.id, lesson_id=lesson.id)

@role_required('student')
@login_required
def student(request):
    course = Course.objects.all()
    return render(request, 'student/student.html', {'course': course})


@role_required('student')
@login_required
def course_view(request, course_id, lesson_id=None):
    # Получаем курс
    course = get_object_or_404(Course, id=course_id)

    # Все уроки курса
    lessons = course.lessons.all()

    selected_lesson = None
    contents = None

    # Если выбран конкретный урок
    if lesson_id:
        selected_lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
        contents = selected_lesson.contents.order_by('order')

    context = {
        'course': course,
        'lessons': lessons,
        'selected_lesson': selected_lesson,
        'contents': contents,
    }
    return render(request, 'student/lesson.html', context)


def custom_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'admin/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def upload_users(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_type = request.POST.get('user_type')
        valid_types = ['teacher', 'student', 'inactive']

        if new_type in valid_types:
            user.user_type = new_type
            user.save()
            messages.success(request, f"Тип пользователя {user.email} обновлён на: {user.get_user_type_display()}")
        else:
            messages.error(request, "Недопустимый тип пользователя.")

        return redirect('users')  # Замените на нужный URL
    return render(request, 'admin/upload_users.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser)
def admin_courses(request):
    courses = Course.objects.all()
    return render(request, 'admin/courses.html', {'courses': courses})