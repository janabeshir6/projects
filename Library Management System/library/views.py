from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from .models import Book, Borrow, Member, Librarybranch
from .forms import CustomUserCreationForm

# View for listing all books
from django.db.models import Q  # Import Q for complex queries

def book_list(request):
    query = request.GET.get('q')  # Get the search query from the URL
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |  # Search by title
            Q(author__icontains=query)  # Search by author
        )
    else:
        books = Book.objects.all()
    
    return render(request, 'library/book_list.html', {'books': books, 'query': query})


# View for borrowing a book
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from .models import Book, Borrow, Member

from django import forms
from django.utils.timezone import now
from datetime import timedelta

# Form for setting return date
class BorrowForm(forms.Form):
    duedate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Set a return date"
    )

@login_required
def borrow_book(request, bookid):
    book = get_object_or_404(Book, pk=bookid)

    if book.stock <= 0:
        messages.error(request, "Sorry, this book is currently unavailable.")
        return redirect('book_list')

    try:
        member = get_object_or_404(Member, email=request.user.email)
    except Member.DoesNotExist:
        messages.error(request, "You are not registered as a library member.")
        return redirect('book_list')

    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            duedate = form.cleaned_data['duedate']

            # Ensure the due date is not in the past
            if duedate <= now().date():
                messages.error(request, "The return date cannot be in the past.")
                return redirect('borrow_book', bookid=bookid)

            Borrow.objects.create(
                bookid=book,
                memberid=member,
                borrowdate=now().date(),
                duedate=duedate
            )
            book.stock -= 1
            book.save()
            messages.success(request, f"You have successfully borrowed '{book.title}' to be returned by {duedate}.")
            return redirect('book_list')
    else:
        form = BorrowForm()

    return render(request, 'library/borrow.html', {'book': book, 'form': form})


# View for registering a new user
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Member, Librarybranch

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Get the selected branch
            branch = form.cleaned_data['branch']

            # Save the new user as a Member with the selected branch
            Member.objects.create(
                name=user.username,
                email=user.email,
                phone='1234567890',  # Replace with actual input if needed
                membershipdate=now().date(),
                branchid=branch  # Save the selected branch
            )

            messages.success(request, "Thank you for registering! You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'library/register.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Borrow, Member
from django.utils.timezone import now

@login_required
def borrowed_books(request):
    try:
        # Get the current member based on the logged-in user's email
        member = Member.objects.get(email=request.user.email)

        # Fetch books borrowed by the member that have not been returned
        borrowed_books = Borrow.objects.filter(memberid=member, returndate__isnull=True).select_related('bookid')

        # Pass the current date for due date comparison in the template
        return render(
            request,
            'library/borrowed_books.html',
            {
                'borrowed_books': borrowed_books,
                'today': now().date(),
            }
        )

    except Member.DoesNotExist:
        messages.error(request, "You are not registered as a library member.")
        return redirect('book_list')

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('book_list')



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Borrow, Book

from django.shortcuts import get_list_or_404

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Borrow, Book, Member
from django.utils.timezone import now

@login_required
def return_book(request, book_id):
    try:
        # Get the current member based on the logged-in user's email
        member = Member.objects.get(email=request.user.email)

        # Fetch the active borrow record (not yet returned) for the specific book and member
        borrow_record = Borrow.objects.filter(bookid=book_id, memberid=member, returndate__isnull=True).first()

        if not borrow_record:
            messages.error(request, "No active borrow record found for the book you are trying to return.")
            return redirect('borrowed_books')

        if request.method == "POST":
            # Update the stock of the book
            book = borrow_record.bookid
            book.stock += 1
            book.save()

            # Check if the return is late and apply the fixed fine
            if now().date() > borrow_record.duedate:
                borrow_record.fineamount = 50  # Fixed fine for late return
                messages.warning(
                    request,
                    f"The book '{book.title}' was returned late. A fine of $50 has been applied."
                )
            else:
                borrow_record.fineamount = 0
                messages.success(request, f"The book '{book.title}' was successfully returned.")

            # Set the return date and save the borrow record
            borrow_record.returndate = now().date()
            borrow_record.save()

            return redirect('borrowed_books')

        # Render the return confirmation page with book details
        return render(request, 'library/return.html', {'book': borrow_record.bookid})

    except Member.DoesNotExist:
        messages.error(request, "You are not registered as a library member.")
        return redirect('book_list')

    except Exception as e:
        # Log unexpected errors and display a generic error message
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('borrowed_books')






from django.shortcuts import render
from .models import Librarybranch

def library_branches(request):

    branches = Librarybranch.objects.all()
    return render(request, 'library/branches.html', {'branches': branches})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    member = get_object_or_404(Member, email=request.user.email)
    return render(request, 'library/profile.html', {'member': member})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UpdateBranchForm
from .models import Member

@login_required
def update_branch(request):
    member = get_object_or_404(Member, email=request.user.email)
    if request.method == 'POST':
        form = UpdateBranchForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch updated successfully!")
            return redirect('profile')
    else:
        form = UpdateBranchForm(instance=member)
    return render(request, 'library/update_branch.html', {'form': form})

from django.shortcuts import render
from .models import Librarybranch

def library_branch_list(request):
    branches = Librarybranch.objects.all()
    return render(request, 'library/library_branch_list.html', {'branches': branches})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
    return render(request, 'library/homepage.html', {'user_name': request.user.username})


# Custom login view to display a success message on login
class CustomLoginView(auth_views.LoginView):
    def form_valid(self, form):
        # Add a success message when login is successful
        messages.success(self.request, "Welcome back! You have successfully logged in.")
        return super().form_valid(form)
