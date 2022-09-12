from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AggregateDriversRevenue

aggregate_api = AggregateDriversRevenue.as_view({
    'get': 'get',
})

# TODO: Create your routers and urls here
router = SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('aggregate', aggregate_api, name="aggregated_drivers_revenue"),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
