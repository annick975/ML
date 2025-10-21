from django.contrib import admin
from .models import Exam, ExamResult

class ExamResultInline(admin.TabularInline):
    model = ExamResult
    extra = 1
    readonly_fields = ('grade', 'created_at', 'updated_at')
    fields = ('student', 'marks_obtained', 'grade', 'remarks')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'subject', 'date', 'start_time', 'end_time', 'location')
    list_filter = ('exam_type', 'subject', 'date')
    search_fields = ('name', 'subject', 'description')
    date_hierarchy = 'date'
    inlines = [ExamResultInline]
    fieldsets = (
        ('Exam Information', {
            'fields': ('name', 'exam_type', 'subject', 'description')
        }),
        ('Schedule', {
            'fields': ('date', 'start_time', 'end_time', 'location')
        }),
        ('Grading', {
            'fields': ('max_marks', 'passing_marks')
        }),
    )

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'marks_obtained', 'grade', 'created_at')
    list_filter = ('grade', 'exam__exam_type', 'exam__subject')
    search_fields = ('exam__name', 'student__username', 'remarks')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('exam', 'student')
        return qs
