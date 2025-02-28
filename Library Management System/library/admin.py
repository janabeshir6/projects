from django.contrib import admin
# Register your models here.
from .models import Book, Genre, Member, Borrow, Shelf, Librarian, Librarybranch, Reservation, Transaction
admin.site.register(Book)
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genreid', 'genrename')  # Display these fields in the admin interface
    search_fields = ('genrename',)  # Enable search functionality by name
admin.site.register(Member)
from django.contrib import admin
from .models import Borrow

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['borrowid', 'bookid', 'memberid', 'borrowdate', 'duedate', 'returndate', 'fineamount']
admin.site.register(Shelf)
admin.site.register(Librarian)
admin.site.register(Librarybranch)
admin.site.register(Reservation)
admin.site.register(Transaction)
