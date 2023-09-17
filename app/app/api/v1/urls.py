from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('wallet/', include('app.api.v1.wallet.urls')),
    path('transaction/', include('app.api.v1.transaction.urls')),
]
