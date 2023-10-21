from django.contrib import admin
from django.db.models.query import QuerySet

from shop.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'amount',
        'status'
    )
    list_filter = ('status',)
    search_fields = (
        'order_id',
        'amount',
        'status'
    )
    list_editable = ('status',)
    list_per_page = 25
    actions = ['mark_as_true', 'mark_as_false']

    def mark_as_true(self, _, queryset: QuerySet):
        queryset.update(status=True)

    mark_as_true.short_description = "Mark selected orders status as true"

    def mark_as_false(self, _, queryset: QuerySet):
        queryset.update(status=False)

    mark_as_false.short_description = "Mark selected orders status as false"
