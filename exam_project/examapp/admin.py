from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Exam, Answer

class ExamAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'ans1', 'ans2', 'ans3', 'ans4')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer_id')

admin.site.register(Exam, ExamAdmin)
admin.site.register(Answer, AnswerAdmin)