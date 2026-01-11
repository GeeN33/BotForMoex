from django.urls import path

from collector_app.views import CollectorQuoterAPIView, BarsAPIView, BarCbrDayAPIView

# collector/symbols/
# collector/bars/<int:id>/
# collector/cbr-bars/CNY/

urlpatterns = [

    path('symbols/', CollectorQuoterAPIView.as_view(), name='collector-symbols'),
    path('bars/<int:id>/', BarsAPIView.as_view(), name='collector-bars'),

    path('cbr-bars/<str:cbr>/', BarCbrDayAPIView.as_view(), name='collector-cbr-bars'),

]