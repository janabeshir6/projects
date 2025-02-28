# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Book(models.Model):
    bookid = models.AutoField(db_column='BookID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isbn = models.CharField(db_column='ISBN', unique=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    genreid = models.ForeignKey('Genre', on_delete=models.CASCADE, db_column='GenreID')
    shelfid = models.ForeignKey('Shelf', on_delete=models.CASCADE, db_column='ShelfID')
    publicationyear = models.IntegerField(db_column='PublicationYear', blank=True, null=True)  # Field name made lowercase.
    stock = models.IntegerField(db_column='Stock', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    def delete(self, *args, **kwargs):
        # Delete all related Borrow records first
        self.borrow_set.all().delete()
        super().delete(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'Book'


class Borrow(models.Model):
    borrowid = models.AutoField(db_column='BorrowID', primary_key=True)  # Correctly set as primary key
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='BookID')  # ForeignKey to Book table
    memberid = models.ForeignKey('Member', models.DO_NOTHING, db_column='MemberID')  # ForeignKey to Member table
    borrowdate = models.DateField(db_column='BorrowDate')
    duedate = models.DateField(db_column='DueDate')
    returndate = models.DateField(db_column='ReturnDate', blank=True, null=True)
    fineamount = models.DecimalField(db_column='FineAmount', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False  # Ensures Django doesn't modify this table
        db_table = 'Borrow'  # Use the existing table name



class Genre(models.Model):
    genreid = models.AutoField(db_column='GenreID', primary_key=True)  # Field name made lowercase.
    genrename = models.CharField(db_column='GenreName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    
    def __str__(self):
        return self.genrename

    class Meta:
        managed = False
        db_table = 'Genre'


class Librarian(models.Model):
    librarianid = models.AutoField(db_column='LibrarianID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    hiredate = models.DateField(db_column='HireDate')  # Field name made lowercase.
    branchid = models.ForeignKey('Librarybranch', on_delete=models.CASCADE, db_column='BranchID')

    class Meta:
        managed = False
        db_table = 'Librarian'


# models.py
class Librarybranch(models.Model):
    branchid = models.AutoField(db_column='BranchID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    location = models.CharField(db_column='Location', max_length=255)
    phone = models.CharField(db_column='Phone', max_length=20)

    def __str__(self):
        return f"{self.name} ({self.location})"

    class Meta:
        managed = False
        db_table = 'LibraryBranch'



class Member(models.Model):
    memberid = models.AutoField(db_column='MemberID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    membershipdate = models.DateField(db_column='MembershipDate')  # Field name made lowercase.
    branchid = models.ForeignKey(Librarybranch, on_delete=models.CASCADE, db_column='BranchID')

    class Meta:
        managed = False
        db_table = 'Member'


class Reservation(models.Model):
    reservationid = models.AutoField(db_column='ReservationID', primary_key=True)  # Field name made lowercase.
    memberid = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='MemberID')
    bookid = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='BookID')
    reservationdate = models.DateField(db_column='ReservationDate')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reservation'


class Shelf(models.Model):
    shelfid = models.AutoField(db_column='ShelfID', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    genreid = models.ForeignKey(Genre, on_delete=models.CASCADE, db_column='GenreID')

    class Meta:
        managed = False
        db_table = 'Shelf'


class Transaction(models.Model):
    transactionid = models.AutoField(db_column='TransactionID', primary_key=True)  # Field name made lowercase.
    borrowid = models.ForeignKey(Borrow, models.DO_NOTHING, db_column='BorrowID')  # Field name made lowercase.
    paymentdate = models.DateField(db_column='PaymentDate')  # Field name made lowercase.
    amountpaid = models.DecimalField(db_column='AmountPaid', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transaction'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
