from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from Books.forms import BookForm
from .forms import ReviewEditForm, BookEditForm
from Books.models import Review, Book


#class ReviewDeleteView(LoginRequiredMixin, ListView):
#    login_url = '/useradmin/login/'
class ReviewDeleteView(ListView):
    model = Review
    context_object_name = 'all_the_reviews'
    template_name = 'review-delete.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewDeleteView, self).get_context_data(**kwargs)
        can_delete = False
        myuser = self.request.user
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        context['can_delete'] = can_delete
        return context

    def post(self, request, *args, **kwargs):
        review_id = request.POST['review_id']
        if 'delete' in request.POST:
            Review.objects.get(id=review_id).delete()
            return redirect('review-delete')


class ReviewEditView(UpdateView):
    model = Review
    form_class = ReviewEditForm
    template_name = 'review-edit.html'
    success_url = reverse_lazy('review-delete')

    def get_context_data(self, **kwargs):
        context = super(ReviewEditView, self).get_context_data(**kwargs)
        can_delete = False
        myuser = self.request.user
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        context['can_delete'] = can_delete
        return context
#@staff_member_required(login_url='/useradmin/login/')


class BookDeleteView(ListView):
    model = Book
    context_object_name = 'all_the_books'
    template_name = 'book-delete.html'

    def get_context_data(self, **kwargs):
        context = super(BookDeleteView, self).get_context_data(**kwargs)
        can_delete = False
        myuser = self.request.user
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        context['can_delete'] = can_delete
        return context

    def post(self, request, *args, **kwargs):
        book_id = request.POST['book_id']
        if 'delete' in request.POST:
            Book.objects.get(id=book_id).delete()
            return redirect('book-delete')


class BookEditView(UpdateView):
    model = Book
    form_class = BookEditForm
    template_name = 'book-edit.html'
    success_url = reverse_lazy('book-delete')

    def get_context_data(self, **kwargs):
        context = super(BookEditView, self).get_context_data(**kwargs)
        can_delete = False
        myuser = self.request.user
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        context['can_delete'] = can_delete
        return context


def book_create(request):
    if request.method == 'POST':
        # print("I am in POST")
        form_in_my_function_based_view = BookForm(request.POST, request.FILES)
        form_in_my_function_based_view.instance.myuser = request.user
        if form_in_my_function_based_view.is_valid():
            form_in_my_function_based_view.save()
            # print("I saved new computergame")
        else:
            pass
            # print(form_in_my_function_based_view.errors)

        return redirect('book-delete')

    else:  # request.method == 'GET'
        # print("I am in GET")
        can_delete = False
        myuser = request.user
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        form_in_my_function_based_view = BookForm()
        context = {'form': form_in_my_function_based_view,
                   'can_delete': can_delete,
                   }
        return render(request, 'book-create.html', context)