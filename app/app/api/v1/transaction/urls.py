from django.urls import path
from app.api.v1.transaction import views

app_name = 'transaction'

urlpatterns = [

    path('',
         view=views.TransactionAPIView.as_view(),
         name='transaction'),
    path('<str:txid>',
         view=views.TransactionRetrieveAPIView.as_view(),
         name='transaction-retrieve'),
]
