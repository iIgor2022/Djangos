from django.contrib import admin

from .models import Student, Teacher


class StudentInLine(admin.TabularInline):
    model = Student
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'group']
    #inlines = [StudentInLine]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']
