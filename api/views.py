from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Book, Borrow, Fine
from .serializers import BookSerializer, BorrowSerializer, FineSerializer
from .permissions import IsAdminUser, IsMember
from rest_framework.decorators import action

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'distroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsMember]
        return [permission() for permission in permission_classes]

class BorrowViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowSerializer
    permission_classes = [IsMember]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Borrow.objects.all()
        return Borrow.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get', 'post'])
    def return_books(self, request, pk=None):
        borrow = self.get_object()
        
        # Return books to stock
        for book in borrow.books.all():
            book.stock += 1
            book.save()
        
        # Calculate and create fine if overdue
        fine_amount = borrow.calculate_fines()
        if fine_amount > 0:
            Fine.objects.create(
                user=borrow.user,
                borrow=borrow,
                amount=fine_amount
            )
        
        borrow.books.clear()
        if borrow.books.count() == 0:
            borrow.delete()
        return Response(status=status.HTTP_200_OK)
    
class FineViewSet(viewsets.ModelViewSet):
    serializer_class = FineSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Fine.objects.all()
        
    @action(detail=True, methods=['post'])   
    def pay(self, request, pk=None):
        fine = self.get_object()
        fine.paid = True
        fine.save()
        return Response(status=status.HTTP_200_OK)



