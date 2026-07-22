from django.urls import path
from .views import VehicleListView, VehicleDetailView

urlpatterns = [
    path(
        'vehicles/',
        VehicleListView.as_view()
    ),

    path(
        'vehicles/<int:pk>/',
        VehicleDetailView.as_view()
    ),
]