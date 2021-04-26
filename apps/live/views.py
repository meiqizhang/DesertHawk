from django.shortcuts import render

# Create your views here.

def live(request):
    return render(request, "live.html")