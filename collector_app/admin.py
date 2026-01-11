from django.contrib import admin

from collector_app.models import ValuteCursCbr, CollectorQuoter, Bar, BarCbr, BarCbrDay


@admin.register(ValuteCursCbr)
class ValuteCursCbrAdmin(admin.ModelAdmin):
    model = ValuteCursCbr
    list_display  = [
        'name',  'updated_at',
    ]
    list_filter = [
        'name',
    ]


@admin.register(CollectorQuoter)
class CollectorQuoterAdmin(admin.ModelAdmin):
    model = CollectorQuoter
    list_display = [
        'symbol_bonds', 'symbol_futures',
    ]

@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    model = Bar


@admin.register(BarCbr)
class BarCbrAdmin(admin.ModelAdmin):
    model = BarCbr
    list_display  = [
        'created_at',
        'cbr_name',
    ]

    list_filter = [
        'cbr__name',
    ]

    def cbr_name(self, obj):
        if obj.cbr:
            return f'{obj.cbr.name} {obj.last} || {obj.last1} | {obj.last2}'


@admin.register(BarCbrDay)
class BarCbrDayAdmin(admin.ModelAdmin):
    model = BarCbrDay
    list_display  = [
        'timestamp',
        'date_str',
        'cbr_price',
    ]

    list_filter = [
        'cbr__name',
    ]

    def cbr_price(self, obj):
        if obj.cbr:
            return f'{obj.cbr.name} {obj.price}'