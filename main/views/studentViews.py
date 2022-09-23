from django.shortcuts import render, redirect

from django.contrib import messages, auth

from django.db.models import Q

from datetime import date, timedelta

from ..models.studentModel import StudentModel

from .. models.usersModel import UsersModel

from ..models.bookModel import BookModel

from ..models.issueBookModel import IssueBookModel


renew = 0

def student_panel(request):
    if request.user.is_authenticated and request.user.is_student:
        return render(request, 'student_template/main.html')

def student_registration(request):
    if request.method == 'POST':
        sname = request.POST.get('name')
        semail = request.POST.get('email')
        smobile = request.POST.get('mobile')
        susername = request.POST.get('username')
        saddress = request.POST.get('address')
        scourse = request.POST.get('course')
        simage = request.FILES.get('image')
        spassword = request.POST.get('password')

        if UsersModel.objects.filter(username=susername).exists():
            messages.info(request, 'This username is already registered!')
            return redirect('/student-registration')
        elif StudentModel.objects.filter(email=semail).exists():
            messages.info(request, 'This email is already registered!')
            return redirect('/student-registration')

        else:
            user = UsersModel.objects.create_student(username=susername, password=spassword)
            user.save()

            #print(user.id)
            sid = user.id
            student = StudentModel.save_student(sid, sname, semail, smobile, saddress, scourse, simage)
            student.save()
            messages.info(request, 'Account is created Successfully.Account Approved by Admin within 5 working days!')
            return redirect('/student-login')

    else:
        return render(request, 'student_template/student_registration_form.html')


def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        #student = StudentModel.objects.get(student_id = user.id)

        if user is not None:
            if user.is_student:
                auth.login(request, user)
                return redirect('/')

        else:
            messages.info(request, 'Invalid user. Please check your credentials!')
            return render(request, 'student_template/login_form.html')
    else:
        return render(request, 'student_template/login_form.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def books(request):
    book = BookModel.all_books()

    context = {'books': book}

    return render(request, 'student_template/books.html', context)


def search_books(request):
    if request.method == 'GET':
        query = request.GET.get('search')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(author__icontains=query) | Q(publication__icontains=query)
            books = BookModel.objects.filter(lookups)
            context = {
                'books': books,
                'query': query
            }

            return render(request, 'student_template/search_books.html', context)
    else:
        return HttpResponse("Search Failed")


def view_profile(request):
    if request.user.is_authenticated and request.user.is_student:
        user = request.user
        student = StudentModel.objects.get(student_id=user.id)

        issue_books = IssueBookModel.objects.filter(student_id=student.id)

        books = []

        

        for b in issue_books:
            book = {}
            bk = BookModel.objects.get(id=b.book_id)
            book['id'] = bk.id
            book['title'] = bk.title
            book['image'] = bk.image
            book['author'] = bk.author
            book['edition'] = bk.edition
            book['rack_no'] = bk.rack_no
            book['issue_date'] = b.issue_date
            book['return_date'] = b.return_date
            books.append(book)

        context = {
            'student': student,
            'username': user.username,
            'books': books,
            'issue_books': issue_books
        }

        return render(request, 'student_template/view_profile.html', context)

    return HttpResponse('<h1>User is not logged in!</h1>')


def renew_book(request, id):
    if request.user.is_authenticated and request.user.is_student:
        user = request.user

        student = StudentModel.objects.get(student_id=user.id)

        issue_book_detail = IssueBookModel.objects.get(book_id = id)

        current_date = date.today()
        return_date = current_date + timedelta(days = 15)

        issue_book_detail.issue_date = current_date
        issue_book_detail.return_date = return_date
        
        issue_book_detail.save()

        messages.info(request, 'Book Renew Successfully')
        return redirect('/view-profile')

    else:
        return HttpResponse('Student is not logged in')
