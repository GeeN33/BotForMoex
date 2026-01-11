from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


# http://localhost:8734/spread/quoter/event/?symbol=CRH6CRM6@RTSX
class EventSpreadQuoterAPIView(APIView):

    def get(self, request):

        symbol = self.request.query_params.get('symbol')

        if symbol:
            unique_id='EventSpreadQuoter'
            # from spread_quoter.tasks import startSpreadQuoterSingle_Task
            # startSpreadQuoterSingle_Task.apply_async(args=[unique_id, symbol])

        return Response({}, status=status.HTTP_200_OK)
