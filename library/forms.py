from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Book, IssuedBook, Note
from .models import PDFDocument


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class BarcodeScanForm(forms.Form):
    barcode_image = forms.ImageField(label='Upload Barcode Image')


class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['name', 'pdf', 'book']

def save(self, commit=True):
        instance = super(NoteForm, self).save(commit=False)
        if self.user:
            instance.user = self.user  # Assign the user to the note if available
        if commit:
            instance.save()
        return instance

class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['enrollment','branch']

class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields=['name','isbn','author','category']

class IssuedBookForm(forms.Form):
    
    isbn2=forms.ModelChoiceField(queryset=models.Book.objects.all(),empty_label="Name and isbn", to_field_name="isbn",label='Name and Isbn')
    enrollment2=forms.ModelChoiceField(queryset=models.StudentExtra.objects.all(),empty_label="Name and enrollment",to_field_name='enrollment',label='Name and enrollment')
    


class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'pdf_file']
