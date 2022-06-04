from django.urls import path
from .views import TransactionDetail, TransactionList

urlpatterns = [
    #path('<int:pk>/', TransactionDetail.as_view()),
    path('transactions/', TransactionDetail),
    path('all-transactions/', TransactionList),

]
