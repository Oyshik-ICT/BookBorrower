from django.contrib import admin
from django.utils.timezone import now
from .models import Book, Borrow, Fine

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'is_stock')
    search_fields = ('title', 'author')
    list_filter = ('stock',)

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('borrow_id', 'user', 'borrow_at', 'return_deadline', 'is_overdue', 'total_fines')
    search_fields = ('user__username', 'borrow_id')
    list_filter = ('borrow_at', 'return_deadline')
    readonly_fields = ('borrow_id', 'total_fines')

    def total_fines(self, obj):
        return obj.calculate_fines()
    total_fines.short_description = 'Calculated Fines'

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('fine_id', 'user', 'borrow', 'amount', 'paid', 'issued_at')
    search_fields = ('user__username', 'fine_id')
    list_filter = ('paid', 'issued_at')
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
    mark_as_paid.short_description = "Mark selected fines as paid"


