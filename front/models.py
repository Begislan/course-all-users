from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError

# Мазмундун түрлөрү
CONTENT_TYPES = (
    ('text', 'Текст'),
    ('image', 'Сүрөт'),
    ('video', 'Видео'),
    ('file', 'Файл'),
)

class Course(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField("Курстун аталышы", max_length=255)
    description = models.TextField("Сүрөттөмө", blank=True)
    image = models.ImageField("Курстун мукабасы", upload_to='course_images/', blank=True, null=True)
    created_at = models.DateTimeField("Түзүлгөн күнү", auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField("Сабактын аталышы", max_length=255)
    order = models.PositiveIntegerField("Тартиби", default=0)
    created_at = models.DateTimeField("Түзүлгөн күнү", auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"

# Тест системасы
class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField("Тесттин аталышы", max_length=255)
    time_limit = models.PositiveIntegerField("Убакыт чектөөсү (мүнөт менен)", default=5)
    pass_percentage = models.PositiveIntegerField("Өтүү упайы (%)", default=70)

    def __str__(self):
        return f"Тест: {self.lesson.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField("Суроо")

    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField("Вариант", max_length=255)
    is_correct = models.BooleanField("Туура жооп", default=False)

    def __str__(self):
        return self.text

# Мазмун (Контент)
class Content(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField("Контенттин түрү", max_length=10, choices=CONTENT_TYPES)
    content_data = models.TextField("Маалымат / Шилтеме / Текст", blank=True)
    file = models.FileField("Файл", upload_to='content_files/', blank=True, null=True)
    order = models.PositiveIntegerField("Тартиби", default=0)

    class Meta:
        ordering = ['order']

# Прогресс жана Тесттин жыйынтыктары
class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField("Аяктады", default=False)
    score = models.FloatField("Тест упайы", default=0.0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.score}%)"

class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] 
# QuizAttempt моделин төмөнкүдөй өзгөртүңүз:
class QuizAttempt(models.Model):
    # Сиздин долбоордо CustomUser колдонулат, ошондуктан бул жерди оңдойбуз:
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField("Упай (%)")
    is_passed = models.BooleanField("Өттү", default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}%)"