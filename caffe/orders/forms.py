from django import forms
from .models import Order, MenuItem


class OrderCreateForm(forms.Form):
    table_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите номер стола'
    }))
    items_input = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите блюда'
    }))


    def clean_table_number(self):
        """
        Проверяет номер таблицы, чтобы убедиться, что он является цифрой и уникален.

        Возвращает:
        int: проверенный номер таблицы.

        Вызывает:
        ValidationError: если номер таблицы не является цифрой или уже существует в базе данных.
        """
        table_number = self.cleaned_data.get('table_number')
        if not table_number.isdigit():
            raise forms.ValidationError("Номер стола должен быть числом!")

        table_number = int(table_number)
        if Order.objects.filter(table_number=table_number).exists():
            raise forms.ValidationError(f"Заказ с номером стола {table_number} уже существует!")
        return table_number

    def clean_items_input(self):
        """
        Проверяет вводимые элементы, чтобы убедиться, что все элементы существуют в меню.

        Возвращает:
        List[MenuItem]: список экземпляров MenuItem, соответствующих вводимым элементам.

        Вызывает:
        ValidationError: если какой-либо из вводимых элементов не найден в меню.
        """
        items_input = self.cleaned_data['items_input']
        item_names = [name.strip() for name in items_input.split(",")]
        menu_items = MenuItem.objects.filter(name__in=item_names)
        if len(menu_items) != len(item_names):
            not_found = set(item_names) - set(menu_items.values_list('name', flat=True))
            raise forms.ValidationError(f"Следующие блюда не найдены: {', '.join(not_found)}")
        return menu_items

    def save(self, commit=True):
        """
        Создает новый заказ из данных формы и сохраняет его в базе данных.

        Аргументы:
        commit (bool): фиксировать ли изменения в базе данных (по умолчанию True).

        Возвращает:
        Order: созданный экземпляр Order.
        """
        table_number = self.cleaned_data['table_number']
        menu_items = self.cleaned_data['items_input']
        order = Order.objects.create(
            table_number=table_number,
            status="pending"
        )
        order.items.set(menu_items)
        total_price = sum(item.price for item in menu_items)
        order.total_price = total_price
        if commit:
            order.save()
        return order


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES)


