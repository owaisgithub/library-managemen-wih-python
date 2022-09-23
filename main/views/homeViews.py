from django.shortcuts import render

def homepage(request):
    return render(request, 'student_template/home.html')