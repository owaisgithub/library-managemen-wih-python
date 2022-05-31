from django.shortcuts import render




def admin_panel(request):
    return render(request, 'admin_panel/dashboard.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        