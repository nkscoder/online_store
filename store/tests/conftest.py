import pytest
from django.contrib.auth.models import User
from store.models import Category, Product, Order

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password123')

@pytest.fixture
def category(db):
    return Category.objects.create(name='Test Category')

@pytest.fixture
def product(db, category):
    return Product.objects.create(name='Test Product', description='Test Description', price=100, stock=10, category=category)

@pytest.fixture
def order(db, user, product):
    order = Order.objects.create(user=user, total_amount=100)
    order.products.add(product)
    return order
