from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('adminclick/', views.adminclick_view),
    path('studentclick/', views.studentclick_view),

    path('book/<int:book_id>/return/', views.return_book, name='return_book'),
    path('viewissuedbookbystudent/', views.viewissuedbookbystudent, name='viewissuedbookbystudent'),
    path('afterlogin/viewissuedbookbystudent/', views.viewissuedbookbystudent, name='viewissuedbookbystudent'),
    path('afterlogin/viewstudent', views.viewstudent_view),
    path('search/', views.search_books, name='search_books'),
    path('issuebook/', views.issuebook_view, name='issuebook'),
    path('afterlogin/search/', views.search_books),
    path('afterlogin/issuebook/', views.issuebook_view, name='issuebook'),
    
    path('adminsignup/', views.adminsignup_view),
    path('studentsignup/', views.studentsignup_view),
    path('adminlogin/', LoginView.as_view(template_name='library/adminlogin.html')),
    path('studentlogin/', LoginView.as_view(template_name='library/studentlogin.html')),
    path('afterlogin/', views.afterlogin_view),

    path('adminclick/adminsignup/', views.adminsignup_view, name='adminsignup'),
    path('adminclick/adminsignup/adminlogin/', LoginView.as_view(template_name='library/adminlogin.html'), name='adminlogin'),
    path('adminclick/adminlogin/adminsignup/', views.adminsignup_view, name='adminsignup'),
    path('adminclick/adminlogin/adminsignup/adminlogin',views.adminsignup_view),
    path('adminclick/adminsignup/adminlogin/adminsignup',views.adminsignup_view),
    path('studentclick/studentsignup/',views.studentsignup_view, name='studentsignup'),
    path('adminclick/adminlogin/', LoginView.as_view(template_name='library/adminlogin.html'), name='adminlogin'),
    path('studentclick/studentlogin/', LoginView.as_view(template_name='library/studentlogin.html'), name='studentlogin'),
    path('studentclick/studentsignup/studentlogin/', LoginView.as_view(template_name='library/studentlogin.html'), name='studentlogin'),
    path('studentclick/studentlogin/studentsignup/', views.studentsignup_view, name='studentsignup'),   
    path('studentclick/studentsignup/studentlogin/studentsignup', views.studentsignup_view), 
    path('studentclick/studentlogin/studentsignup/studentlogin/', LoginView.as_view(template_name='library/studentlogin.html'), name='studentlogin'), 
    
    path('delete-pdf/<int:pdf_id>/', views.delete_pdf, name='delete_pdf'),
    path('delete-pdf/<int:pdf_id>/', views.delete_pdf, name='delete_pdf'),
    
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls') ),
    path('add-pdf/', views.add_pdf, name='add_pdf'),
    path('', views.home_view),
    path('upload/', views.add_pdf, name='add_pdf'),
    path('pdf-list/', views.pdf_list, name='pdf_list'),


    path('logout', LogoutView.as_view(template_name='library/index.html')),
    path('afterlogin/', views.afterlogin_view),

    path('afterlogin/addbook', views.addbook_view),
    path('afterlogin/viewbook/', views.viewbook_view),
    path('afterlogin/issuebook/', views.issuebook_view),
    path('afterlogin/viewissuedbook/', views.viewissuedbook_view),
    path('afterlogin/issuebook/viewissuedbook/', views.viewissuedbook_view),
    path('afterlogin/viewstudent', views.viewstudent_view),
    path('addbook/', views.addbook_view),
    path('viewbook/', views.viewbook_view),
    path('issuebook/', views.issuebook_view),
    path('viewissuedbook/', views.viewissuedbook_view),
    path('viewstudent/', views.viewstudent_view),
    path('viewissuedbookbystudent/', views.viewissuedbookbystudent),
    path('issuebook/viewissuedbook', views.viewissuedbook_view),
    path('issuebook/issuebook', views.issuebook_view),
    path('admin/delete-book/<int:book_id>/', views.delete_book_view, name='delete_book'),

    path('about_us/', views.aboutus_view),
    path('stuabout_us/', views.aboutus_view),
    path('adminabout_us/', views.aboutus_view),

    path('contactus/', views.contactus_view),
    path('logout/',views.logout_view,name="logout")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
