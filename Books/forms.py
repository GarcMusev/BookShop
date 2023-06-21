from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Book, Review


class BookForm(forms.ModelForm):  #Die Form des zu erstellenden Buch Objektes

    class Meta:
        model = Book
        fields = ['title', 'subtitle', 'author', 'genre', 'type', 'description', 'price', 'pages', 'date_published', 'book_picture', 'book_pdf']  #Genaue Reihenfolge zum Ausfüllen
        widgets = {
            'type': forms.Select(choices=Book.BOOK_TYPES),  #DropDown Menü für den Typ
            'genre': forms.Select(choices=Book.BOOK_GENRES),  # DropDown Menü für den Typ
            'creation_time': forms.HiddenInput(),
            'myuser': forms.HiddenInput(),  #Den User der sieht mann nicht
            'review_rating': forms.HiddenInput(),
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['text', 'star_rating']
        widgets = {
            'myuser': forms.HiddenInput(),
            'book': forms.HiddenInput(),
        }

class SearchForm(forms.ModelForm):

    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    review_rating = forms.IntegerField(required=False)

    class Meta:
        model = Book
        fields = ['title', 'description', 'review_rating']

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            self.fields['review_rating'].required = False