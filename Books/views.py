from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView

from Shoppingcart.models import ShoppingCart
from .forms import BookForm, ReviewForm, SearchForm
from .models import Book, Review


class BookListView(ListView):  #Erben von ListView
    model = Book
    context_object_name = 'all_the_books'  # Default: object_list, dies kann man benutzen um durch alle Books in der Liste zu iterieren
    template_name = 'book-list.html'  # Default: book_list.html


def book_detail(request, **kwargs):  #Erben von DateilView
    print(kwargs)
    book_id = kwargs['pk']

    print('book_id', book_id)

    book = Book.objects.get(id=book_id)

    reviews = Review.objects.filter(book=book)  #Alle Reviews von einem Buch
    reviews_number = Review.objects.filter(myuser=request.user, book=book)    #die Anzahl der reviews von einem Nutzer

    counter = 0
    counter2 = 0
    for review in reviews:  # Gehe mit ner ForSchleife alle Reviews durch
        counter += review.star_rating  #Addition der Stars
        counter2 += 1

    if counter >= 1:
        book.review_rating = counter / counter2    #Weise den Wert des counters dem book Model zu
        book.save() #update das Attribut
    else:
        book.review_rating = counter

    context = {'that_one_book': book,
               'myuser': request.user,
               'reviews_for_that_one_book': reviews,
               'Number_of_stars': book.review_rating}    #Gebe den Counter zurÃ¼ck

    if reviews_number.count() == 1:
        return render(request, 'book-detail.html', context)

    # Add comment
    if request.method == 'POST':
        if "edit" in request.POST:
            form = ReviewForm(request.POST)
            form.instance.myuser = request.user
            form.instance.book = book
            if form.is_valid():
                form.save()
                reviews = Review.objects.filter(book=book)  # Alle Reviews von einem Buch  # die Anzahl der reviews von einem Nutzer

                counter = 0
                counter2 = 0
                for review in reviews:  # Gehe mit ner ForSchleife alle Reviews durch
                    counter += review.star_rating  # Addition der Stars
                    counter2 += 1

                if counter >= 1:
                        book.review_rating = counter / counter2  # Weise den Wert des counters dem book Model zu
                        book.save()  # update das Attribut
                else:
                        book.review_rating = counter

                context = {'that_one_book': book,
                           'myuser': request.user,
                           'reviews_for_that_one_book': reviews,
                            'Number_of_stars': book.review_rating}
                return render(request, 'book-detail.html', context)
            else:
                print(form.errors)
                print('Es wurden zu viele Sterne abgegeben, bitte bleiben SIe zwischen 0 und 5')

        elif "add" in request.POST:
            form = ReviewForm(request.POST)
            form.instance.myuser = request.user
            form.instance.book = book
            ShoppingCart.add_item(form.instance.myuser, book)


    context['review_form'] = ReviewForm
    return render(request, 'book-detail.html', context)


def book_review_delete(request, **kwargs):
    review_id = kwargs['pk']

    if request.method == 'POST':
        that_review = Review.objects.get(id=review_id)  #Extrahiere die CGame ID von dem Comment der gelöscht werden soll

        Review.objects.get(id=review_id).delete() #Lösche den eigentlichen Kommentar

        return redirect('book-detail', that_review.get_bookid_from_review())  #Wechsel beim erfolgreichem löschen, zurück zur DetailAnsicht mit der zuvor ausgewählten CGame ID
    else:
        that_one_review_in_my_view = Review.objects.get(id=review_id)
        context = {'that_one_review': that_one_review_in_my_view,
                   }
        return render(request, 'book-review-delete.html', context)


class BookCreateView(CreateView):  #Erben von CreateView
    model = Book
    form_class = BookForm
    template_name = 'book-create.html'  # Default: book_form.html
    success_url = reverse_lazy('book-list')  #Nimmt den namen book-list und geht zur genauen Book Url in Books/urls.py

    def form_valid(self, form):  # Die fehlende User Information wird nachträglich ergänzt
        form.instance.myuser = self.request.user
        return super().form_valid(form)


def book_search(request):
    if request.method == 'POST':
        search_string_title = request.POST['title']
        books_found = Book.objects.filter(title__contains=search_string_title)

        search_string_description = request.POST['description']
        if search_string_description:
            books_found = Book.objects.filter(description__contains=search_string_description)

        search_string_rating = request.POST['review_rating']
        if search_string_rating:
            books_found = books_found.filter(review_rating__contains=search_string_rating)

        form_in_function_based_view = SearchForm()
        context = {'form': form_in_function_based_view,
                   'books_found': books_found,
                   'show_results': True}
        return render(request, 'book-search.html', context)

    else:
        form_in_function_based_view = SearchForm()
        context = {'form': form_in_function_based_view,
                   'show_results': False}
        return render(request, 'book-search.html', context)


def vote(request, pk: str, up_or_down: str):
    review = Review.objects.get(id=int(pk))

    print('review', review)
    myuser = request.user
    book_id = review.book.id

    review.vote(myuser, up_or_down)
    return redirect('book-detail', pk=book_id)


def review_edit(request, pk, pkReview):
    review = Review.objects.get(id=pkReview)
    if review.myuser == request.user:
        form = ReviewForm(instance=review)
    else:
        return redirect('book-detail', pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('book-detail', pk)

    context = {'form': form}
    return render(request, 'book-review-edit.html', context)
