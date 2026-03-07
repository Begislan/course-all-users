from django.contrib import admin
from front.models import Course, Lesson, Content, Quiz, Question, Choice

# 1. Варианттарды (Choices) суроонун ичинде көрсөтүү үчүн
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4  # Дароо 4 бош вариант талаасын көрсөтөт
    fields = ['text', 'is_correct'] # Варианттын тексти жана туура/ката белгиси

# 2. Суроолорду (Questions) тесттин ичинде көрсөтүү үчүн
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1  # Жаңы тест түзүүдө 1 суроо талаасын дароо чыгарат
    show_change_link = True # Суроонун өзүнө өтүп кетүүчү шилтеме

# --- Негизги моделдерди каттоо ---

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'course']
    list_filter = ['course']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'time_limit', 'pass_percentage']
    inlines = [QuestionInline] # Тесттин ичинде суроолорду кошуу

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz']
    inlines = [ChoiceInline] # Суроонун ичинде варианттарды кошуу

# Башка калган моделдер
admin.site.register(Content)
admin.site.register(Choice) # Керек болсо өзүнчө да көрсө болот