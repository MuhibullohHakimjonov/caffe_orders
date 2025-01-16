from django.test import TestCase

from .forms import OrderCreateForm
from .models import Order, MenuItem


# Тестирование модели

from django.test import TestCase
from .models import Order, MenuItem


class OrderModelTest(TestCase):

    def setUp(self):
        self.menu_item_1 = MenuItem.objects.create(name='Суп', price=100)
        self.menu_item_2 = MenuItem.objects.create(name='Салат', price=150)

    def test_order_creation(self):
        order = Order.objects.create(table_number=1, status='pending')
        order.items.set([self.menu_item_1, self.menu_item_2])
        order.total_price = sum(item.price for item in order.items.all())
        order.save()

        self.assertEqual(order.total_price, 250)  # Проверяем, что цена правильная
        self.assertEqual(order.status, 'pending')

    def test_order_status_change(self):
        order = Order.objects.create(table_number=2, status='pending')
        order.status = 'paid'
        order.save()

        self.assertEqual(order.status, 'paid')



# Тестирование форм

class OrderCreateFormTest(TestCase):

	def setUp(self):
		# Создаём тестовые блюда в базе данных
		self.menu_item_1 = MenuItem.objects.create(name='Суп', price=100)
		self.menu_item_2 = MenuItem.objects.create(name='Салат', price=150)

	def test_valid_form(self):
		data = {
			'table_number': '1',
			'items_input': 'Суп, Салат'
		}
		form = OrderCreateForm(data)
		self.assertTrue(form.is_valid())

	def test_invalid_table_number(self):
		data = {
			'table_number': 'abc',
			'items_input': 'Суп, Салат'
		}
		form = OrderCreateForm(data)
		self.assertFalse(form.is_valid())
		self.assertIn('Номер стола должен быть числом!', form.errors['table_number'])

	def test_items_not_found(self):
		data = {
			'table_number': '1',
			'items_input': 'Суп, Несуществующее блюдо'
		}
		form = OrderCreateForm(data)
		self.assertFalse(form.is_valid())
		self.assertIn('Следующие блюда не найдены:', form.errors['items_input'][0])

	def test_duplicate_table_number(self):
		Order.objects.create(table_number=1, status='pending')

		data = {
			'table_number': '1',
			'items_input': 'Суп, Салат'
		}
		form = OrderCreateForm(data)
		self.assertFalse(form.is_valid())
		self.assertIn(f"Заказ с номером стола 1 уже существует!", form.errors['table_number'])






# Тестирование представлений


from django.urls import reverse



class OrderViewTest(TestCase):

    def setUp(self):
        self.menu_item_1 = MenuItem.objects.create(name='Суп', price=100)
        self.menu_item_2 = MenuItem.objects.create(name='Салат', price=150)
        self.order = Order.objects.create(table_number=1, status='pending')
        self.order.items.set([self.menu_item_1, self.menu_item_2])
        self.order.save()

    def test_order_list_view(self):
        response = self.client.get(reverse('all_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Суп')
        self.assertContains(response, 'Салат')
        self.assertContains(response, 'В ожидании')

    def test_order_create_view(self):
        data = {
            'table_number': '2',
            'items_input': 'Суп, Салат'
        }
        response = self.client.post(reverse('create_order'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 2)

    def test_change_status_view(self):
        data = {'status': 'ready'}
        response = self.client.post(reverse('order_detail', args=[self.order.id]), data)
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'ready')






