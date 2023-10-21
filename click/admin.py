from django.contrib import admin
from django.db.models.query import QuerySet

from click.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'click_trans_id',
        'merchant_trans_id',
        'amount',
        'action',
        'status'
    )
    list_filter = ('status',)
    search_fields = (
        'click_trans_id',
        'merchant_trans_id',
        'amount',
        'action',
        'status'
    )
    list_editable = ('status',)
    list_per_page = 25
    actions = ['mark_as_finished', 'mark_as_canceled']

    def mark_as_finished(self, _, queryset: QuerySet):
        queryset.update(status='finished')

    mark_as_finished.short_description = "Mark selected transactions as finished"

    def mark_as_canceled(self, _, queryset: QuerySet):
        queryset.update(status='canceled')

    mark_as_canceled.short_description = "Mark selected transactions as canceled"
