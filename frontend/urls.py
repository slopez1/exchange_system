from django.urls import path
from .views import *


app_name = 'frontend'

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('data/<gb_pk>/', DataDetail.as_view(), name='global_data_detail'),
    path('requesters/', Requesters.as_view(), name='requesters_data'),
    path('share_data/', CreateData.as_view(), name='create_data'),
    path('own_data/', OwnData.as_view(), name='own_data'),
    path('own_data/<data_pk>/', OwnDataDetail.as_view(), name='own_data_detail'),
]
