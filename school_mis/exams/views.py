from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def exam_list(request):
    """View for listing all exams."""
    context = {
        'title': 'Exam Management',
        'active_page': 'exams',
    }
    return render(request, 'exams/exam_list.html', context)
