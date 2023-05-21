import os
import random
import uuid
from calendar import monthrange
from django.utils.timezone import now as timezone_now
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

def filename_ext(filepath):
    file_base = os.path.basename(filepath)
    filename, ext = os.path.splitext(file_base)
    return filename, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 9498594795)
    name, ext = filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "pictures/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class Ministry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    leader = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MemberManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def active(self):
        qs = self.get_queryset().filter(active=True)
        return qs

    def deleted(self):
        return self.get_queryset().filter(active=False)

    def pays_tithe(self):
        return self.active().filter(pays_tithe=True)

    def working(self):
        return self.active().filter(working=True)

    def schooling(self):
        return self.active().filter(schooling=True)


class Member(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this member should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        }
    )
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=255, null=True, blank=True)
    mothers_name = models.CharField(max_length=255, null=True, blank=True)
    guardians_name = models.CharField(max_length=255, null=True, blank=True)
    pays_tithe = models.BooleanField(
        help_text=_(
            "Designates whether this member should pay tithe. "
            "Unselecting this means Members wont be pay tithe."
        ),
        default=True
    )
    is_working = models.BooleanField(
        help_text=_(
            "Designates whether this member is currently working"
        ),
      default=False
    )
    is_schooling = models.BooleanField(
        help_text=_(
            "Designates whether this member is currently a student"
        ),
        default=False
    )
    picture = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = MemberManager()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    ref_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.description} - {self.amount}"


class Category(models.Model):
    INCOME = 'I'
    EXPENDITURE = 'E'

    CATEGORY_CHOICES = [
        (INCOME, 'Income'),
        (EXPENDITURE, 'Expenditure'),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f'{self.name} - type: {self.get_type_display()}'


class Income(Transaction):
    pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        account:Account = Account.objects.first()
        if account:
            account.balance += self.amount
            account.save()

    def __str__(self):
        return f"Income: {self.description} - {self.amount}"


class Expenditure(Transaction):
    recipient = models.CharField(max_length=255)

    def __str__(self):
        return f"Expenditure: {self.description} - {self.amount}"

    def save(self, *args, **kwargs):
        account_balance = Account.get_balance()
        if self.amount > account_balance:
            raise ValueError("Insufficient account balance to create this expenditure.")
        super().save(*args, **kwargs)
        # Update the account balance after saving the expenditure
        Account.objects.update(balance=models.F('balance') - self.amount)


class Account(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_incomes(self):
        return Income.objects.all()

    def get_expenditures(self):
        return Expenditure.objects.all()

    def get_tithes(self):
        return Tithe.objects.all()

    @classmethod
    def get_balance(cls):
        account = cls.objects.first()
        if account:
            return account.balance
        return 0

    @classmethod
    def create_account_for_new_month(cls):
        current_month = timezone_now().month
        account = cls.objects.filter(created_at__month=current_month).first()
        if not account:
            last_month_account = cls.objects.order_by('-created_at').first()
            new_account = cls.objects.create(balance=last_month_account.balance)
            new_account.save()
            print("New account created for the new month.")

    def __str__(self):
        return f"Account Balance: {self.balance}"


class Tithe(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    ref_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        account:Account = Account.objects.first()
        if account:
            account.balance += self.amount
            account.save()

    def __str__(self):
        return f"Tithe - Amount: {self.amount}, Date: {self.date}"


Account.create_account_for_new_month()
