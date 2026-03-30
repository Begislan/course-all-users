from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError

# Мазмундун түрлөрү
CONTENT_TYPES = (
    ('text', 'Текст'),
    ('image', 'Сүрөт (Файл)'),
    ('video', 'Видео (YouTube шилтеме)'),
    ('video_file', 'Видео (MP4 Файл)'),
    ('file', 'Документ/Файл'),
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

class Content(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField("Контенттин түрү", max_length=15, choices=CONTENT_TYPES)
    content_data = models.TextField("Текст же Видео шилтемеси", blank=True, null=True)
    file = models.FileField("Компьютерден жүктөө", upload_to='lesson_contents/', blank=True, null=True)
    order = models.PositiveIntegerField("Тартиби", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Сабактын мазмуну"
        verbose_name_plural = "Сабактын мазмундары"

    def __str__(self):
        return f"{self.lesson.title} - {self.get_content_type_display()} ({self.order})"

    def clean(self):
        # image_244157.jpg скриншотундагы логика боюнча оңдолду
        if self.content_type == 'text' and not self.content_data:
            raise ValidationError("Текст түрү тандалса, текст жазылышы керек.")
        if self.content_type in ['image', 'file', 'video_file'] and not self.file:
            raise ValidationError(f"{self.get_content_type_display()} үчүн файл тандалышы керек.")

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

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField("Упай (%)")
    is_passed = models.BooleanField("Өттү", default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Сактоо алдында упай жетиштүүбү же жокпу автоматтык түрдө текшерет
        if self.score >= self.quiz.pass_percentage:
            self.is_passed = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}%)"
class QuizSessionImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='proctoring_shots/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Прокторинг сүрөтү"
        verbose_name_plural = "Прокторинг сүрөттөрү"

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.created_at.strftime('%H:%M:%S')})"