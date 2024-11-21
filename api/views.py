from typing import Any, List, Optional

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Book, Borrow, Fine
from .permissions import IsAdminUser, IsMember
from .serializers import BookSerializer, BorrowSerializer, FineSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing book operations with role-based permissions.

    """

    queryset: List[Book] = Book.objects.all()
    serializer_class: BookSerializer = BookSerializer

    def get_permissions(self) -> List[Any]:
        """
        Dynamically set permissions based on action type.

        """
        try:
            if self.action in ["create", "update", "partial_update", "distroy"]:
                permission_classes: List[Any] = [IsAdminUser]
            else:
                permission_classes: List[Any] = [IsMember]
            return [permission() for permission in permission_classes]
        except Exception as e:
            print(f"Permission Error: {str(e)}")


class BorrowViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing book borrowing operations.
    """

    serializer_class: BorrowSerializer = BorrowSerializer
    permission_classes: List[Any] = [IsMember]

    def get_queryset(self) -> List[Borrow]:
        """
        Retrieve borrow records based on user role.
        """
        try:
            if self.request.user.is_staff:
                return Borrow.objects.all()
            return Borrow.objects.filter(user=self.request.user)
        except Exception as e:
            print(f"Queryset Retrieval Error: {str(e)}")

    @action(detail=True, methods=["get", "post"])
    def return_books(self, request: Request, pk: Optional[int] = None) -> Response:
        """
        Process book return, update stock, and calculate potential fines.
        """
        try:
            borrow: Borrow = self.get_object()

            # Return books to stock
            for book in borrow.books.all():
                book.stock += 1
                book.save()

            # Calculate and create fine if overdue
            fine_amount = borrow.calculate_fines()
            if fine_amount > 0:
                Fine.objects.create(user=borrow.user, borrow=borrow, amount=fine_amount)

            borrow.books.clear()
            if borrow.books.count() == 0:
                borrow.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Book Return Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing fine operations.
    """

    serializer_class: FineSerializer = FineSerializer
    queryset: List[Fine] = Fine.objects.all()
    permission_classes: List[Any] = [IsAdminUser]

    @action(detail=True, methods=["post"])
    def pay(self, request: Request, pk: Optional[int] = None) -> Response:
        """
        Mark a fine as paid.
        """
        try:
            fine = self.get_object()
            fine.paid = True
            fine.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Fine Payment Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
