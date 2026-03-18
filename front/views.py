from django.http import Http404 
from django.http import HttpResponseForbidden
from accounts.models import CustomUser as User, CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Lesson, Content ,  Quiz, Question, Choice, UserProgress , Comment , QuizAttempt
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
    # views.py
@login_required
@role_required('student')
def student(request):
    course_list = Course.objects.all()
    
    for cour in course_list:
        total_lessons = cour.lessons.count()
        # Курстун биринчи сабагын алуу (url түзүү үчүн керек)
        first_lesson = cour.lessons.order_by('order').first()
        cour.first_lesson_id = first_lesson.id if first_lesson else None
        
        # ... калган прогресс эсептөө логикаңыз ...
        completed_count = UserProgress.objects.filter(user=request.user, lesson__course=cour).count()
        cour.progress_percent = int((completed_count / total_lessons) * 100) if total_lessons > 0 else 0
            
    return render(request, 'student/student.html', {'course': course_list})
# --- САБАКТЫ КӨРҮҮ ЖАНА ПРОГРЕСС ---
# --- САБАКТЫ КӨРҮҮ ЖАНА ПРОГРЕСС ---
@login_required
@role_required('student')
def course_view(request, course_id, lesson_id=None):
    course = get_object_or_404(Course, id=course_id)
    # Сабактарды ирети менен алуу
    lessons = list(course.lessons.all().order_by('order'))
    
    if not lessons:
        return render(request, 'student/lesson.html', {'course': course, 'lessons': []})

    # 1. КУЛПУЛОО ЛОГИКАСЫ (Locking system)
    for i, lesson in enumerate(lessons):
        if i == 0:
            lesson.is_locked = False  # Биринчи сабак дайыма ачык
        else:
            prev_lesson = lessons[i-1]
            if hasattr(prev_lesson, 'quiz'):
                # Тесттен өткөнүн текшерүү (мисалы, 60%дан жогору упай алса)
                passed = QuizAttempt.objects.filter(
                    user=request.user, 
                    quiz=prev_lesson.quiz, 
                    score__gte=prev_lesson.quiz.pass_percentage
                ).exists()
                lesson.is_locked = not passed
            else:
                # Эгер мурунку сабакта тест жок болсо, сабак ачык
                lesson.is_locked = False

    # Тандалган сабакты аныктоо
    if lesson_id:
        selected_lesson = next((l for l in lessons if l.id == int(lesson_id)), lessons[0])
    else:
        selected_lesson = lessons[0]
        
    # Эгер окуучу кулпуланган сабакка шилтеме аркылуу кирүүгө аракет кылса, 
    # аны ачык турган акыркы сабакка кайтаруу:
    if selected_lesson.is_locked:
        return redirect('course_view', course_id=course.id)

    # Тест барбы же жокпу
    has_quiz = hasattr(selected_lesson, 'quiz')

    # Прогрессти белгилөө
    UserProgress.objects.get_or_create(user=request.user, lesson=selected_lesson)

    # Контенттер жана Кадамдар (Steps)
    contents = list(selected_lesson.contents.all().order_by('order'))
    step_index = int(request.GET.get('step', 0))
    if step_index < 0: step_index = 0
    if contents and step_index >= len(contents): step_index = len(contents) - 1
    current_content = contents[step_index] if contents else None

    # Навигация (Кийинки/Артка)
    current_idx = lessons.index(selected_lesson)
    next_lesson = lessons[current_idx + 1] if current_idx < len(lessons) - 1 else None
    
    # Прогресс пайызы (Бардык сабактар / бүткөн сабактар)
    total_l = len(lessons)
    done_l = UserProgress.objects.filter(user=request.user, lesson__course=course, is_completed=True).count()
    progress_percent = int((done_l / total_l) * 100) if total_l > 0 else 0

    # КОММЕНТАРИЙЛЕР (AJAX колдоосу менен)
    if request.method == 'POST':
        text = request.POST.get('comment')
        if text:
            comment = Comment.objects.create(lesson=selected_lesson, user=request.user, text=text)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'user': comment.user.username,
                    'text': comment.text,
                    'initial': comment.user.username[0].upper()
                })
            return redirect(request.path)

    context = {
        'course': course,
        'lessons': lessons,
        'selected_lesson': selected_lesson,
        'has_quiz': has_quiz,
        'quiz': getattr(selected_lesson, 'quiz', None),
        'contents': contents,
        'current_content': current_content,
        'step_index': step_index,
        'next_lesson': next_lesson,
        'comments': selected_lesson.comments.all().order_by('-created_at'),
        'progress_percent': progress_percent,
    }
    return render(request, 'student/lesson.html', context)
# --- ТЕСТТИ АЛУУ ---
# views.py ичиндеги POST логикасын толуктайбыз
@login_required
@role_required('student')
def take_quiz(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quiz = get_object_or_404(Quiz, lesson=lesson)
    questions = quiz.questions.all()

    if request.method == 'POST':
        correct_answers = 0
        total_questions = questions.count()

        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                is_correct = Choice.objects.filter(
                    id=selected_choice_id, 
                    question=question, 
                    is_correct=True
                ).exists()
                if is_correct:
                    correct_answers += 1

        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # --- ЭҢ МААНИЛҮҮ ЖЕР: QuizAttempt сактоо ---
        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score_percentage
        )

        # Прогрессти жаңыртуу
        is_passed = score_percentage >= quiz.pass_percentage
        UserProgress.objects.update_or_create(
            user=request.user, 
            lesson=lesson,
            defaults={
                'score': score_percentage,
                'is_completed': is_passed # Эгер упай жетсе True болот
            }
        )

        return render(request, 'teacher/quiz_result.html', {
            'score': score_percentage, 
            'quiz': quiz,
            'is_passed': is_passed, # Шаблондо колдонуу үчүн
            'correct_answers': correct_answers,
            'total_questions': total_questions
        })

    return render(request, 'teacher/quiz.html', {
        'quiz': quiz, 
        'questions': questions,
        'lesson': lesson
    })
@login_required
@role_required('teacher')
def add_quiz(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # 1. Эгер бул сабакта тест бар болсо, UNIQUE катасын болтурбоо үчүн текшеребиз
    if hasattr(lesson, 'quiz'):
        return redirect('lesson_detail', course_id=lesson.course.id, lesson_id=lesson.id)

    if request.method == 'POST':
        # Тесттин негизги маалыматтарын алуу
        title = request.POST.get('title')
        pass_percentage = request.POST.get('pass_percentage', 60)
        time_limit = request.POST.get('time_limit', 30)
        
        # 2. Тестти түзүү
        quiz = Quiz.objects.create(
            lesson=lesson,
            title=title,
            pass_percentage=pass_percentage,
            time_limit=time_limit
        )

        # 3. Суроолорду динамикалык түрдө сактоо
        # Шаблондогу 'q_text_0', 'q_text_1' ж.б. алуу үчүн индекс колдонобуз
        q_index = 0
        while f'q_text_{q_index}' in request.POST:
            q_text = request.POST.get(f'q_text_{q_index}')
            
            if q_text:
                # Суроону сактоо
                question = Question.objects.create(quiz=quiz, text=q_text)
                
                # Туура жооптун индекси (0, 1, 2 же 3)
                correct_idx = request.POST.get(f'correct_for_q_{q_index}')
                
                # 4. Бул суроонун 4 вариантын сактоо
                for c_index in range(4):
                    choice_text = request.POST.get(f'choice_q_{q_index}_{c_index}')
                    if choice_text:
                        Choice.objects.create(
                            question=question,
                            text=choice_text,
                            is_correct=(str(c_index) == correct_idx)
                        )
            q_index += 1

        # Баары сакталгандан кийин сабактын барагына кайтабыз
        return redirect('lesson_detail', course_id=lesson.course.id, lesson_id=lesson.id)

    return render(request, 'teacher/add_quiz.html', {'lesson': lesson})

@login_required
@role_required('teacher')
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        
        # Суроону түзүү
        if question_text:
            question = Question.objects.create(quiz=quiz, text=question_text)
            
            # Жоопторду сактоо (4 вариант деп эсептейли)
            for i in range(1, 5):
                choice_text = request.POST.get(f'choice_{i}')
                # radio баскычынан келген маанини текшерүү
                is_correct = (request.POST.get('is_correct') == str(i))
                
                if choice_text:
                    Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
        
        # "Кийинки суроо" басылса кайра ушул эле баракка жиберет
        return redirect('add_question', quiz_id=quiz.id)
            
    return render(request, 'teacher/add_question.html', {'quiz': quiz})