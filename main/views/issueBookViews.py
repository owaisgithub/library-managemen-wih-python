from django.shortcuts import render, redirect

from django.contrib import messages

from django.http import HttpResponse

from datetime import date

from ..models.usersModel import UsersModel

from ..models.bookModel import BookModel

from ..models.studentModel import StudentModel

from ..models.issueBookModel import IssueBookModel

def issue_book(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        book = BookModel.objects.get(id = id)

        if request.method == 'POST':
            #book_id = request.POST.get('book_id')
            username = request.POST.get('username')
            user = UsersModel.objects.get(username=username)

            student = StudentModel.objects.get(student_id = user.id)

            if student.tag == 'blacklisted':
                messages.info(request, 'This student is blacklisted.')
                return redirect('/%d/issue-book'%book.id)

            elif student.tag == 'cancelled':
                messages.info(request, 'This student account has been cancelled.')
                return redirect('/%d/issue-book'%book.id)

            else:
                issue_book = IssueBookModel.issue_book(book.id, student.id)
                issue_book.save()

                book.no_of_copy -= 1

                book.save()

                messages.info(request, 'Book Issued!')
                return redirect('/%d/issue-book'%book.id)
        else:
            #messages,info(request, 'Book is not issue')
            context = {'book':book}
            return render(request, 'admin_panel/issue_book.html', context)

    return HttpResponse('Admin is not logged in')



def view_issue_books(request):
    if request.user.is_authenticated and request.user.is_admin:
        issue_books = IssueBookModel.get_all()

        books = []

        for b in issue_books:
            book = {}
            bk = BookModel.objects.get(id=b.book_id)
            st = StudentModel.objects.get(id=b.student_id)
            book['id'] = bk.id
            book['username'] = UsersModel.objects.get(id=st.student_id).username
            book['title'] = bk.title
            book['image'] = bk.image
            book['author'] = bk.author
            book['edition'] = bk.edition
            book['rack_no'] = bk.rack_no
            book['issue_date'] = b.issue_date
            book['return_date'] = b.return_date
            books.append(book)

        context = {
            'books': books,
            'issue_books': issue_books
        }

        return render(request, 'admin_panel/issue_book_details.html', context)

    else:
        return HttpResponse('Admin is not logged in')


def return_book(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            username = request.POST.get('username')

            user = UsersModel.objects.get(username=username)
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
                'username': username,
                'books': books,
                'issue_books': issue_books
            }

            return render(request, 'admin_panel/return_book.html', context)

        else:
            return render(request, 'admin_panel/return_book.html')


def returned(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        issue_book_detail = IssueBookModel.objects.get(book_id = id)

        book = BookModel.objects.get(id=id)

        student = StudentModel.objects.get(id = issue_book_detail.student_id)

        return_date = issue_book_detail.return_date

        current_date = date.today()

        if return_date < current_date:
            delta = current_date - return_date
            days = delta.days

            fine = days * 10

            student.fine = fine

            student.save()
            issue_book_detail.delete()
            book.no_of_copy += 1
            book.save()

            return redirect('/return-book')

        else:
            issue_book_detail.delete()
            book.no_of_copy += 1
            book.save()
            return redirect('/return-book')


    return HttpResponse('Admin is not logged in')

