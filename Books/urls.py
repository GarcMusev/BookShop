from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.book_search, name='books-search'),
    path('show/', views.BookListView.as_view(), name='book-list'),
    path('show/<int:pk>/', views.book_detail, name='book-detail'),  #Zeige genau das Buch mit dem eingegebenen PrimaryKey
    path('show/<int:pk>/edit/<int:pkReview>', views.review_edit, name='book-review-edit'),
    path('deleteReview/<int:pk>/', views.book_review_delete, name='book-review-delete'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='book-review-vote'),
]