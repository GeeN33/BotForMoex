from django.contrib import admin

from spread_quoter.models import BotQuoterSpread, OrderSmartSpread


@admin.register(OrderSmartSpread)
class OrderSmartSpreadAdmin(admin.ModelAdmin):
    model = OrderSmartSpread
    list_filter = [
        'bot',
    ]


class OrderSmartSpreadInLine(admin.StackedInline):
    model = OrderSmartSpread
    extra = 0

@admin.register(BotQuoterSpread)
class BotQuoterSpreadAdmin(admin.ModelAdmin):
    model = BotQuoterSpread
    inlines = [OrderSmartSpreadInLine, ]
