from django.shortcuts import render

# Create your views here.
from apps.statistic.views import add_visit


@add_visit
def about(request):
    return render(request, 'templates/about.html')
