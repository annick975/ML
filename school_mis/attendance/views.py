from time import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date, timedelta
from .models import Attendance, Student
from attendance.forms import StudentForm


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('attendance:add_student')
        
    else:
        form = StudentForm()
    return render(request, 'attendance/add_student.html', {'form': form})


def mark_attendance(request):
    if request.method == 'POST':
        # Handle attendance submission
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
        attendance_date = request.POST.get('date')
        
        if student_id and status and attendance_date:
            student = get_object_or_404(Student, id=student_id)
            # Convert status to boolean (assuming 'present' is the only truthy value)
            is_present = (status == 'present')
            Attendance.objects.update_or_create(
                student=student,
                date=attendance_date,
                defaults={'present': is_present}
            )
            return redirect('attendance:mark_attendance')
    
    # For GET requests or if POST data is invalid
    today = date.today()
    students = Student.objects.all().order_by('name')
    
    if not students.exists():
        # If no students exist, redirect to add student page
        return redirect('attendance:add_student')
    
    # Get today's attendance status for each student
    attendance_data = []
    for student in students:
        attendance = Attendance.objects.filter(
            student=student,
            date=today
        ).first()
        attendance_data.append({
            'student': student,
            'attendance': attendance
        })
    
    return render(request, 'attendance/mark_attendance.html', {
        'attendance_data': attendance_data,
        'today': today
    })


def attendance_list(request):
    # Get filter parameters
    classroom = request.GET.get('classroom', '')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Start with all attendance records
    records = Attendance.objects.select_related('student').order_by('-date')
    
    # Apply filters
    if classroom:
        records = records.filter(student__classroom__iexact=classroom)
    
    if date_from:
        records = records.filter(date__gte=date_from)
    
    if date_to:
        records = records.filter(date__lte=date_to)
    
    # Get unique classrooms for filter dropdown
    classrooms = Student.objects.values_list('classroom', flat=True).distinct()
    
    # Get attendance statistics
    total_students = Student.objects.count()
    present_count = records.filter(present=True).count()
    absent_count = records.filter(present=False).count()
    
    context = {
        'records': records[:100],  # Limit to 100 records for performance
        'classrooms': classrooms,
        'selected_classroom': classroom,
        'date_from': date_from or (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'date_to': date_to or date.today().strftime('%Y-%m-%d'),
        'total_students': total_students,
        'present_count': present_count,
        'absent_count': absent_count,
        'active_page': 'attendance',
    }
    
    return render(request, 'attendance/attendance_list.html', context)