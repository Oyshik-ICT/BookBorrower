from typing import Dict, List

from django.db.models import Count
from rest_framework import serializers

from .models import Book, Borrow, Fine


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model, includes validation for the price field.
    """

    class Meta:
        model = Book
        fields = "__all__"

    def validate_price(self, value: int) -> int:
        """
        Validate that the price is greater than zero.
        """
        if value <= 0:
            raise serializers.ValidationError("Price should be greater than zero")
        return value


class BorrowSerializer(serializers.ModelSerializer):
    """
    Serializer for Borrow model, handles borrowing logic and fine calculations.
    """

    books = BookSerializer(many=True, read_only=True)
    book_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    fine_amount = serializers.SerializerMethodField()

    class Meta:
        model = Borrow
        fields = (
            "borrow_id",
            "user",
            "books",
            "book_ids",
            "borrow_at",
            "return_deadline",
            "fine_amount",
            "is_overdue",
        )
        read_only_fields = (
            "borrow_id",
            "user",
            "borrow_at",
            "return_deadline",
            "fine_amount",
            "is_overdue",
        )

    def get_fine_amount(self, obj: Borrow) -> int:
        """
        Calculate the fine amount for a borrow instance.
        """
        return obj.calculate_fines()

    def create(self, validated_data: Dict) -> Borrow:
        """
        Create a new borrow instance and handle book stock updates.
        """
        book_ids: List[int] = validated_data.pop("book_ids")

        if len(book_ids) == 0:
            raise serializers.ValidationError("You have to borrow more than zero book")

        user = self.context["request"].user

        # Check borrow limit
        current_borrows: int = (
            Borrow.objects.filter(user=user, books__isnull=False).aggregate(
                total_books=Count("books")
            )["total_books"]
            or 0
        )

        if current_borrows + len(book_ids) > 5:
            raise serializers.ValidationError(
                "Cannot borrow more than 5 books at a time"
            )

        # borrow = Borrow.objects.create(user=user, **validated_data)
        books = Book.objects.filter(id__in=book_ids)

        # Check stock availability
        for book in books:
            if not book.is_stock:
                raise serializers.ValidationError(
                    f"Book '{book.title}' is out of stock"
                )

        for book in books:
            book.stock -= 1
            book.save()
        borrow = Borrow.objects.create(user=user, **validated_data)
        borrow.books.set(books)
        return borrow


class FineSerializer(serializers.ModelSerializer):
    """
    Serializer for Fine model.
    """
    
    class Meta:
        model = Fine
        fields = "__all__"
        read_only_fields = ("fine_id", "user", "amount", "issued_at")
