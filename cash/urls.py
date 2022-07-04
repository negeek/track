from django.urls import path
from .views import CategoriesView, CategoryView, TransactionView, TransactionsView
# CategoryCreateView
urlpatterns = [
    #path('categories/create/', CategoryCreateView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('categories/<int:id>/', CategoryView.as_view()),
    path('transactions/', TransactionsView.as_view()),
    path('transactions/<int:id>/', TransactionView.as_view()),

    #path('transactions/', TransactionDetail),
    #path('all-transactions/', TransactionList),

]
