from django.urls import path

from collector_app.views import CollectorQuoterAPIView, BarsAPIView, BarCbrDayAPIView
from spread_quoter.views import EventSpreadQuoterAPIView

# spread/quoter/event/


urlpatterns = [

    path('event/', EventSpreadQuoterAPIView.as_view(), name='spread-quoter-event'),

]