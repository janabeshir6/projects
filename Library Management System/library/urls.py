from django.urls import path
from . import views


urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('register/', views.register, name='register'),  # Add this line
    path('borrow/<int:bookid>/', views.borrow_book, name='borrow_book'),
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),  # Added URL
    path('library_branch/', views.library_branch_list, name='library_branch'),



]
