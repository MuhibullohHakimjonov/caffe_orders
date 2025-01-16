from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import OrderCreateForm, OrderStatusForm
from django.db.models import Q
from django.db.models import Sum
from django.views.generic import ListView
from django.views import View




class OrderListView(ListView):
    model = Order
    template_name = 'orders/index.html'
    context_object_name = 'orders'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '').strip()
        status_filter = self.request.GET.get('status', '').strip()
        orders = Order.objects.all()

        if search_query or status_filter:
            filters = Q()
            # Фильтрация по номеру стола
            if search_query.isdigit():
                filters &= Q(table_number__icontains=search_query)

            # Фильтрация по статусу
            if status_filter:
                status_translation = {
                    'в ожидании': 'pending',
                    'готово': 'ready',
                    'оплачено': 'paid',
                }
                translated_status = status_translation.get(status_filter.lower())
                if translated_status:
                    filters &= Q(status=translated_status)

            orders = orders.filter(filters)

        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context



def create_order(request):
	"""
	    Создает новый заказ с уникальным идентификатором, суммой заказа и статусом.

	    Параметры:
	    table_number (int): Номер стола, с которого был сделан заказ.
	    items (List[str]): Список названий блюд, выбранных для заказа.

	    Возвращает:
	    Dict[str, str]: Словарь с информацией о заказе, включая ID, статус и цену.
	    """
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('all_orders')
	else:
		form = OrderCreateForm()
	return render(request, 'orders/create_order.html', {'form': form})





class DeleteOrderView(View):
	def post(self, request, order_id):
		order = get_object_or_404(Order, id=order_id)
		order.delete()
		return redirect('all_orders')



def order_detail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	if request.method == 'POST':
		form = OrderStatusForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('all_orders')
	else:
		form = OrderStatusForm(instance=order)
	return render(request, 'orders/order_detail.html', {'form': form, 'order': order})


def revenue_report(request):
	"""
	Вычисляет общий доход от заказов со статусом «оплачено» и отображает его в шаблоне.

	Аргументы:
	request (HttpRequest): объект HTTP-запроса.

	Возвращает:
	HttpResponse: обработанный ответ, содержащий общий доход.
	"""
	total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum'] or 0
	return render(request, 'orders/revenue_report.html', {'total_revenue': total_revenue})



