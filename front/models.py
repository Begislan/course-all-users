from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError

# Выбор типов контента
CONTENT_TYPES = (
    ('text', 'Текст'),
    ('image', 'Изображение'),
    ('video', 'Видео'),
    ('file', 'Файл'),
)

class Course(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField("Название курса", max_length=255)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Обложка курса", upload_to='course_images/', blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField("Название урока", max_length=255)
    order = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError('Размер файла не должен превышать 5 МБ.')


class Content(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField("Тип контента", max_length=10, choices=CONTENT_TYPES)
    content_data = models.TextField("Содержимое / ссылка / текст")
    file = models.FileField("Файл", upload_to='content_files/', blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_content_type_display()} - {self.lesson.title}"
        # ... (мурунку моделдер)

class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Жаңылары өйдө жакта турат

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
    # Бул модель студенттин кайсы сабакты бүтүргөнүн сактайт
class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Бир студент бир сабакты бир эле жолу "бүттү" деп белгилеши керек
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} аяктады: {self.lesson.title}"
    
