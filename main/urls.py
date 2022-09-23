from django.urls import path

from .views import homeViews, bookViews, studentViews, adminViews, issueBookViews


urlpatterns = [
    path('', homeViews.homepage),
    #admin urls
    path('admin-login/', adminViews.admin_login),
    path('admin-panel/', adminViews.admin_panel),
    path('admin-logout/', adminViews.logout),
    path('add-book/', bookViews.add_book),
    path('show-books/', bookViews.get_books),
    path('<int:id>/update-book/', bookViews.update_book),
    path('<int:id>/delete/', bookViews.delete_view),
    path('<int:id>/issue-book/', issueBookViews.issue_book),
    path('return-book/', issueBookViews.return_book),
    path('<int:id>/returned/', issueBookViews.returned),
    path('view-issue-book', issueBookViews.view_issue_books),
    path('change-password/', adminViews.change_password),
    path('create-admin/', adminViews.create_admin),
    path('<int:id>/approved/', adminViews.approved_student),
    path('<int:id>/rejected/', adminViews.rejected_student),
    path('manage-student/', adminViews.manage_student),
    path('<int:id>/cancelled/', adminViews.student_cancel),
    path('<int:id>/blacklisted/', adminViews.student_blacklist),
    path('<int:id>/active/', adminViews.student_active),

    #student urls
    path('student-panel/', studentViews.student_panel),
    path('student-registration/', studentViews.student_registration),
    path('student-login/', studentViews.student_login),
    path('student-logout/', studentViews.logout),
    path('books/', studentViews.books),
    path('search-books/', studentViews.search_books),
    path('view-profile/', studentViews.view_profile),
    path('<int:id>/renew', studentViews.renew_book),
]