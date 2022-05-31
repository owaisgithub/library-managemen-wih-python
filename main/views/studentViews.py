from django.shortcuts import render


def student_registration(request):
    if request.method == 'POST':

        return render(request, 'templ.html')

    else:
        return render(request, 'student_template/student_registration_form.html')