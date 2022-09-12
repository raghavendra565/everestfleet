# TODO: Create your views here.
from django.http import JsonResponse
from django.core.paginator import Paginator
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from datetime import datetime
import logging
import sys

from rest_framework import viewsets

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import FleetDailyTrips

logger = logging.getLogger(__name__)

start_date = openapi.Parameter('start_date', openapi.IN_QUERY, "start date param format should be yyyy-mm-dd", type=openapi.TYPE_STRING)
end_date = openapi.Parameter('end_date', openapi.IN_QUERY, "end date param format should be yyyy-mm-dd", type=openapi.TYPE_STRING)
page = openapi.Parameter('page', openapi.IN_QUERY, "page param. default is 0", type=openapi.TYPE_INTEGER)
page_size = openapi.Parameter('page_size', openapi.IN_QUERY, "page size param. default is 50", type=openapi.TYPE_INTEGER)
sort = openapi.Parameter('sort', openapi.IN_QUERY, "sort by param `revenue` or `total_trips`", type=openapi.TYPE_STRING)
sort_dir = openapi.Parameter('sort_dir', openapi.IN_QUERY, "sorting direction either `asc` or `desc`", type=openapi.TYPE_STRING)

@permission_classes((AllowAny,))
class AggregateDriversRevenue(viewsets.ModelViewSet):

    # @csrf_exempt
    @swagger_auto_schema(
        operation_description="API to aggregate drivers revenue",
        manual_parameters=[start_date, end_date, page, page_size, sort, sort_dir])
    def get(self, request):
        """API to get aggregated drivers revenue"""
        try:
            page_number = int(request.GET.get("page")) if request.GET.get("page") is not None else 0
            page_size = int(request.GET.get("page_size")) if request.GET.get("page_size") is not None else 50
            sort = request.GET.get("sort").lower() if request.GET.get("sort") is not None else "revenue"
            sort_dir = request.GET.get("sort_dir").lower() if request.GET.get("sort_dir") is not None else "asc"
            start_date = request.GET.get("start_date")
            end_date = request.GET.get("end_date")
            start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date is not None else None
            end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date is not None else None
            if sort_dir not in ["asc", "desc"]:
                return JsonResponse({"message": "invalid query parameters for sort_dir - {}".format(sort_dir), 
                    "success": False}, status=500)
            if sort not in ["revenue", "total_trips"]:
                return JsonResponse({"message": "invalid query parameters for sort - {}".format(sort), 
                    "success": False}, status=500)
            if start_date and end_date:
                daily_trips = FleetDailyTrips.objects.filter(date__gte=start_date, date__lt=end_date)
            else:
                daily_trips = FleetDailyTrips.objects.all()
            paginator = Paginator(daily_trips, page_size)
            page = paginator.get_page(page_number+1)
            records = []
            drivers = {}
            for row in page:
                if row.driver_id is None:
                    continue
                if row.driver_id not in drivers:
                    drivers[row.driver_id] = {
                        "revenue": row.cash_collected,
                        "driver_id": row.driver_id,
                        "total_trips": row.trips
                    }
                else:
                    drivers[row.driver_id]["revenue"] += row.cash_collected
                    drivers[row.driver_id]["total_trips"] += row.trips
            drivers = [driver for driver in drivers.values()]
            if sort_dir == "desc":
                drivers.sort(key=lambda rec: rec[sort], reverse=True)
            else:
                drivers.sort(key=lambda rec: rec[sort])
            return JsonResponse({"data": drivers, "success": True})
        except Exception as error:
            *_, exc_tb = sys.exc_info()
            logger.error(" Type & error: " + str(error.__repr__()) +
                        " Reason: " + str(error.__doc__) +
                        " Line No: " + str(exc_tb.tb_lineno))
            return JsonResponse({"message": "internal_server_error", 
                "more_info": str(error), 'success': False}, status=500)

