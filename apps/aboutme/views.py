from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.user.views import add_visit_history_log


@add_visit_history_log
def about(request):
    return render(request, 'templates/about.html')
