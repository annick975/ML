from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Render the main dashboard view."""
    context = {
        'title': 'School MIS Dashboard',
        'active_page': 'dashboard',
        'user': request.user,
    }
    return render(request, 'dashboard/dashboard.html', context)
