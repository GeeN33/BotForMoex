from django.contrib import admin

from bund_quoter.models import OrderQuoter, BotQuoter


@admin.register(OrderQuoter)
class OrderQuoterAdmin(admin.ModelAdmin):
    model = OrderQuoter
    list_filter = [
        'bot',
    ]


class OrderQuoterInLine(admin.StackedInline):
    model = OrderQuoter
    extra = 0


@admin.register(BotQuoter)
class BotQuoterAdmin(admin.ModelAdmin):
    model = BotQuoter
    inlines = [OrderQuoterInLine, ]
