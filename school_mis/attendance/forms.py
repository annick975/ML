from django import forms
from django.forms import widgets
from .models import Student, Attendance

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'classroom']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder' : 'Enter student name'
            }),
            'classroom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ENter classroom name'
            }),
        }