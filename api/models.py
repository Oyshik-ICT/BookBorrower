import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta


def default_return_deadline():
    return now() + timedelta(days=14)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    @property
    def is_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.title


class Borrow(models.Model):
    borrow_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrows")
    books = models.ManyToManyField(Book, related_name="borrowed_books")
    borrow_at = models.DateTimeField(auto_now_add=True)
    return_deadline = models.DateTimeField(default=default_return_deadline)

    @property
    def is_overdue(self):
        return now() > self.return_deadline

    def calculate_fines(self):
        if self.is_overdue:
            overdue_days = (now() - self.return_deadline).days
            fine_rate = 5
            return overdue_days * fine_rate
        return 0

    def __str__(self):
        return f"Borrow ID: {self.borrow_id} - User: {self.user.username}"


class Fine(models.Model):
    fine_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fines")
    borrow = models.OneToOneField(Borrow, on_delete=models.CASCADE, related_name="fine")
    amount = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Paid" if self.paid else "Unpaid"
        return f"Fine {self.fine_id} - User: {self.user.username} - {status}"
