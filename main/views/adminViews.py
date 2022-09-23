from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib import auth, messages

from django.contrib.auth.hashers import make_password

from django.core.mail import send_mail

from django.template.loader import render_to_string

from ..forms.adminForm import AdminForm

from ..models.bookModel import BookModel

from ..models.usersModel import UsersModel

from ..models.studentModel import StudentModel

from ..models.issueBookModel import IssueBookModel

from datetime import date



def admin_panel(request):
    if request.user.is_authenticated and request.user.is_admin:
        books_no = len(BookModel.all_books())

        req_student = StudentModel.requested_student()
        no_req_student = len(req_student)

        no_active_student = StudentModel.active_student_no()
 
        no_bl_student = StudentModel.blacklisted_student_no()

        no_cn_student = StudentModel.cancelled_student_no()

        no_issue_books = len(IssueBookModel.get_all())

        no_today_issue = IssueBookModel.today_issue_books_no()



        context = {
            'total_book':books_no,
            'req_student': req_student,
            'no_req_student': no_req_student,
            'no_active_student': no_active_student,
            'no_bl_student': no_bl_student,
            'no_cn_student': no_cn_student,
            'no_issue_books':no_issue_books,
            'no_today_issue':no_today_issue

        }
        return render(request, 'admin_panel/dashboard.html', context)
    else:
    	return HttpResponse('<div align="center" style="margin-top:200px;"><h2>Admin is not Login</h2><a href="/admin-login">go to login page</a></div>')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
        	if user.is_admin:
	        	auth.login(request, user)
	        	return redirect('/admin-panel')

        else:
        	messages.info(request, 'Invalid User! Please check your credentials')
        	return render(request, 'admin_panel/login_form.html')     
            
    return render(request, 'admin_panel/login_form.html')
    

def logout(request):
    auth.logout(request)
    return redirect('/')


def create_admin(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = UsersModel.objects.create_superuser(username=username, password=password)
            user.save()
            messages.info(request, 'Admin is Created!')
            return redirect('/create-admin')
        else:
            return render(request, 'admin_panel/create_admin.html')
            
    else:
        return HttpResponse("Failed")


def change_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if request.user.is_authenticated and request.user.is_admin:
            if password1 == password2:
                admin = UsersModel.objects.get(id = request.user.id)

                admin.password = make_password(password1)
                admin.save()
                messages.info(request, 'Password Created')
                return redirect('/change-password')

            else:
                messages.info(request, 'Password does not match')
                return redirect('/change-password')

        else:
            return HttpResponse("User Is not login!")

    else:
        return render(request, 'admin_panel/change_password.html')




def approved_student(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        user = UsersModel.objects.get(id = id)
        student = StudentModel.objects.get(student_id = id)

        user.is_staff = True
        user.save()

        student.tag = 'active'
        student.save()

        subject = "Student Account has been approved"
        message = 'Your account has been approved. Please login with your username and password.'
        to_email = student.email

        msg_html = render_to_string('email.html', {'name': student.name})

        send_mail(
            subject, 
            message, 
            'owaismfos@gmail.com', 
            [to_email], 
            fail_silently=False,
            html_message=msg_html
            )

        print('mail sent')
        return redirect('/admin-panel')
    else:
        return HttpResponse('Failed')


def rejected_student(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        user = UsersModel.objects.get(id = id)
        student = StudentModel.objects.get(student_id = id)

        user.delete()
        student.delete()

        return redirect('/admin-panel')
    else:
        return HttpResponse('Failed')


def manage_student(request):
    if request.user.is_authenticated and request.user.is_admin:
        student_active = StudentModel.get_all_active()
        student_blacklist = StudentModel.get_all_blacklisted()
        student_cancel = StudentModel.get_all_cancelled()

        context = {
            'active': student_active,
            'blacklist': student_blacklist,
            'cancel': student_cancel
        }

        return render(request, 'admin_panel/manage_student.html', context)

    else:
        return HttpResponse("Admin is not logged in")

def student_cancel(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        student = StudentModel.objects.get(student_id = id)

        student.tag = 'cancelled'

        student.save()

        return redirect('/manage-student')

    else:
        return HttpResponse('Admin is not logged in')

def student_blacklist(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        student = StudentModel.objects.get(student_id = id)

        student.tag = 'blacklisted'

        student.save()

        return redirect('/manage-student')

    else:
        return HttpResponse('Admin is not logged in')

def student_active(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        student = StudentModel.objects.get(student_id=id)

        student.tag = "active"

        student.save()

        return redirect('/manage-student')
    else:
        return HttpResponse('Admin is not logged in')

