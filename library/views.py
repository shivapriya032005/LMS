from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from librarymanagement.settings import EMAIL_HOST_USER
from django.contrib.auth import logout
from django.db.models import Q
from .forms import IssuedBookForm, NoteForm
from .models import IssuedBook, StudentExtra
from .models import Book, Note
from .forms import PDFDocumentForm
from .models import PDFDocument


@login_required(login_url='studentlogin')
def delete_pdf(request, pdf_id):
    pdf_document = get_object_or_404(PDFDocument, id=pdf_id)
    if request.method == 'POST':
        pdf_document.delete()
        return redirect('pdf_list')
    return redirect('pdf_list')

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})

def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    
    form=forms.BookForm()
    if request.method=='POST':
        
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})


def search_books(request):
    query = request.GET.get('query')
    books = []

    if query:
        books = Book.objects.filter(
            Q(name__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()

    return render(request, 'library/search_results.html', {'books': books})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'library/viewbook.html',{'books':books})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            student_enrollment = request.POST.get('enrollment2')
            current_borrowed_count = IssuedBook.objects.filter(enrollment=student_enrollment).count()
            
            if current_borrowed_count >= 4:
                return render(request, 'library/too_many_books.html')
            
            obj = models.IssuedBook()
            obj.enrollment = student_enrollment
            obj.isbn = request.POST.get('isbn2')
            obj.save()
            return render(request, 'library/issuebook.html')
    return render(request, 'library/issuebook.html', {'form': form})

@login_required(login_url='studentlogin')
def add_pdf(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request,'library/studentafterlogin.html')
    else:
        form = NoteForm()
    return render(request, 'add_pdf.html', {'form': form})



@login_required(login_url='studentlogin')
def add_notes_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list')  # Redirect to the PDF list page
    else:
        form = NoteForm()
    return render(request, 'library/add_notes.html', {'form': form})

@login_required(login_url='studentlogin')
def add_pdf(request):
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list')
    else:
        form = PDFDocumentForm()
    return render(request, 'library/add_pdf.html', {'form': form})

@login_required(login_url='studentlogin')
def pdf_list(request):
    pdf_documents = PDFDocument.objects.all()
    return render(request, 'library/pdf_list.html', {'pdf_documents': pdf_documents})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        
        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)
    return render(request,'library/viewissuedbook.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_book_view(request, book_id):
    li=[]
    book = get_object_or_404(models.Book, id=book_id)
    book.delete()
    return redirect(request,'library/viewissuedbook.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook = models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1 = []
    li2 = []

    for ib in issuedbook:
        books = models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t = (request.user, student[0].enrollment, student[0].branch, book.name, book.author)
            li1.append(t)
        issdate = f"{ib.issuedate.day}-{ib.issuedate.month}-{ib.issuedate.year}"
        expdate = f"{ib.expirydate.day}-{ib.expirydate.month}-{ib.expirydate.year}"
        days = (date.today() - ib.issuedate).days
        fine = 0
        if days > 15:
            day = days - 15
            fine = day * 10
        t = (issdate, expdate, fine, book.id)  
        li2.append(t)

    return render(request, 'library/viewissuedbookbystudent.html', {'li1': li1, 'li2': li2})

@login_required(login_url='studentlogin')
def return_book(request, book_id):
    try:
        issued_book = get_object_or_404(models.IssuedBook, isbn=book_id, enrollment=request.user.studentextra.enrollment)
        if request.method == "POST":
            issued_book.delete()  
            return redirect('viewissuedbookbystudent')
    except models.IssuedBook.DoesNotExist:
        return HttpResponse("Book not issued or already returned.")

    return HttpResponse("Invalid request method.")


def aboutus_view(request):
    user_role = request.session.get('user_role', 'student')  
    
    if user_role == 'admin':
        return render(request, 'library/adminabout_us.html')
    else:
        return render(request, 'library/stuabout_us.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['shivapriya032005@gmail.com'], fail_silently = False)
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form':sub})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
