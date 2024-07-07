from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta

class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40, unique=True)
    branch = models.CharField(max_length=40)
    #used in issue book
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('scifi','Sci-Fi')
        ]
    name = models.CharField(max_length=200 , default='Untitled Book')
    isbn = models.PositiveIntegerField()
    author = models.CharField(max_length=40)
    category = models.CharField(max_length=30,choices=catchoice,default='education')
    available = models.BooleanField(default=True)
    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'

def get_expiry():
    return datetime.today() + timedelta(days=15)

class IssuedBook(models.Model):

    enrollment=models.CharField(max_length=30)

    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self):
        return self.enrollment
    
class Note(models.Model):
    name = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='notes_pdfs/', default='path/to/default/file.pdf')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='notes')

class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title