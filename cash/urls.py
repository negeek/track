from django.urls import path
from .views import CategoriesView, CategoryView, TransactionView, TransactionsView, DebitCreditView, DateFilterView
from django.urls import path, register_converter, re_path
from cash.converters import DateConverter


urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('categories/<int:id>/', CategoryView.as_view()),
    path('transactions/', TransactionsView.as_view()),
    path('transactions/<int:id>/', TransactionView.as_view()),
    path('transactions/<str:transaction_type>/', DebitCreditView.as_view()),
    path('transactions/date/<int:start_year>/<int:start_month>/<int:start_day>/',
         DateFilterView.as_view()),
    path('transactions/date/<int:start_year>/<int:start_month>/<int:start_day>/<int:end_year>/<int:end_month>/<int:end_day>/',
         DateFilterView.as_view()),

]
