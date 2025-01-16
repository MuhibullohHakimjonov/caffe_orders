from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
	path('', OrderListView.as_view(), name='all_orders'),
	path('orders/change-status/<int:order_id>/', order_detail, name='order_detail'),
	path('create-order/', create_order, name='create_order'),
	path('order/delete/<int:order_id>/', DeleteOrderView.as_view(), name='delete_order'),
	path('revenue-report/', revenue_report, name='revenue_report'),

]
