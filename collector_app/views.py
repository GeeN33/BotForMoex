from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from collector_app.models import Bar, CollectorQuoter, BarCbrDay
from collector_app.serializers import CollectorQuoterSerializer, BarSerializer, BarCbrDaySerializer


# http://localhost:8733/collector/symbols/
# http://localhost:8733/collector/bars/1/

class CollectorQuoterAPIView(ListAPIView):
    serializer_class = CollectorQuoterSerializer
    queryset = CollectorQuoter.objects.all()


class BarsAPIView(APIView):

    def get(self, request, id):

        try:
            bars = Bar.objects.select_related('collector').filter(collector_id=id)
        except Bar.DoesNotExist:

            return Response({}, status=status.HTTP_200_OK)

        data =  BarSerializer(bars, many=True).data


        return Response(data, status=status.HTTP_200_OK)



class BarCbrDayAPIView(APIView):

    def get(self, request, cbr):

        try:
            bars = BarCbrDay.objects.filter(cbr__name=cbr)
        except BarCbrDay.DoesNotExist:

            return Response({}, status=status.HTTP_200_OK)

        data =  BarCbrDaySerializer(bars, many=True).data


        return Response(data, status=status.HTTP_200_OK)
