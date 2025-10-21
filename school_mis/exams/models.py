from django.db import models
from django.contrib.auth import get_user_model

class Exam(models.Model):
    EXAM_TYPES = [
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('test', 'Test'),
    ]
    
    name = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    subject = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    max_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_exam_type_display()} ({self.date})"

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam', 'student')

    def save(self, *args, **kwargs):
        # Auto-calculate grade based on percentage
        percentage = (self.marks_obtained / self.exam.max_marks) * 100
        if percentage >= 90:
            self.grade = 'A+'
        elif percentage >= 80:
            self.grade = 'A'
        elif percentage >= 70:
            self.grade = 'B'
        elif percentage >= 60:
            self.grade = 'C'
        elif percentage >= 50:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.exam.name} ({self.marks_obtained}/{self.exam.max_marks})"
