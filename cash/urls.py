from django.urls import path
from .views import TransactionDetail

urlpatterns = [
    #path('<int:pk>/', TransactionDetail.as_view()),
    path('transactions/', TransactionDetail),

]
