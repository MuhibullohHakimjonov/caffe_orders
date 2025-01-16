from django.db import models



class MenuItem(models.Model):
    name = models.CharField("Название блюда", max_length=100)
    price = models.DecimalField("Цена блюда", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.price}сум)"


class Order(models.Model):
    """
       Модель для создания заказов.
       Содержит информацию о номере стола, статусе, стоимости и связанных блюдах.

       Attributes:
           table_number (int): Номер стола.
           status (str): Статус заказа (например, "pending", "ready", "paid").
           total_price (float): Общая стоимость заказа.
           items (ManyToManyField): Связь с блюдами, выбранными в заказе.
       """
    table_number = models.IntegerField()
    items = models.ManyToManyField('MenuItem', related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'В ожидании'),
            ('ready', 'Готово'),
            ('paid', 'Оплачено'),
        ],
        default='pending',
    )

    def __str__(self):
        return f'{self.table_number} - {self.status}'


