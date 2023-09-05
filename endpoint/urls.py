from django.urls import path
from .views import *

app_name = 'endpoint'

urlpatterns = [
    path('<data_pk>/', GetDataView.as_view(), name='data_detail'),
]
