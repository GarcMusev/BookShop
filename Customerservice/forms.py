from django import forms
from Books.models import Review, Book


class ReviewEditForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'review_id': forms.HiddenInput(),
        }


class BookEditForm(forms.ModelForm):  #Die Form des zu erstellenden Buch Objektes

    class Meta:
        model = Book
        fields = ['title', 'subtitle', 'author', 'genre', 'type', 'description', 'price', 'pages', 'date_published', 'book_picture', 'book_pdf']  #Genaue Reihenfolge zum Ausfüllen
        widgets = {
            'type': forms.Select(choices=Book.BOOK_TYPES),  #DropDown Menü für den Typ
            'genre': forms.Select(choices=Book.BOOK_GENRES),  # DropDown Menü für den Typ
            'creation_time': forms.HiddenInput(),
            'myuser': forms.HiddenInput(),  #Den User der sieht mann nicht
            'review_rating': forms.HiddenInput(),
            'book_id': forms.HiddenInput(),
        }