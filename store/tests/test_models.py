import pytest
from store.models import Category, Product, Order

@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name='Test Category')
    assert str(category) == 'Test Category'

@pytest.mark.django_db
def test_product_str():
    category = Category.objects.create(name='Test Category')
    product = Product.objects.create(name='Test Product', description='Test Description', price=100, stock=10, category=category)
    assert str(product) == 'Test Product'

@pytest.mark.django_db
def test_product_stock_decrease(product):
    initial_stock = product.stock
    product.decrease_stock(5)
    assert product.stock == initial_stock - 5

@pytest.mark.django_db
def test_order_str(order):
    assert str(order) == f'Order #{order.id}'

@pytest.mark.django_db
def test_order_total_amount(order):
    assert order.total_amount == 100

@pytest.mark.django_db
def test_order_product_quantity(order, product):
    assert order.products.count() == 1
    assert product.stock == 10

@pytest.mark.django_db
def test_order_product_association(order, product):
    assert order.products.filter(id=product.id).exists()
