from django.urls import path
from app.api.v1.wallet import views

app_name = 'wallet'

urlpatterns = [

    path('',
         view=views.WalletAPIView.as_view(),
         name='wallet'),
    path('<int:pk>/',
         view=views.WalletRetrieveAPIView.as_view(),
         name='wallet-retrieve'),
    path('deposit/',
         view=views.WalletDepositAPIView.as_view(),
         name='wallet-deposit'),
    path('withdraw/',
         view=views.WalletWithdrawAPIView.as_view(),
         name='wallet-withdraw'),

]
