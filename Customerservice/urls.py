from django.urls import path
from . import views

urlpatterns = [
    path('delete/comment/', views.ReviewDeleteView.as_view(), name='review-delete'),
    path('edit/comment/<int:pk>/', views.ReviewEditView.as_view(), name='review-edit'),
    path('create/', views.book_create, name='book-create'),
    path('delete/book/', views.BookDeleteView.as_view(), name='book-delete'),
    path('edit/book/<int:pk>/', views.BookEditView.as_view(), name='book-edit'),
]