from django.shortcuts import render

# Create your views here.

def list(request):
    context = {}
    return render(request, "linking.html", context=context)  # 只返回页面，数据全部通过ajax获取
