import pytest
from rest_framework.test import APIClient
from store.models import Product, Order,OrderProduct



@pytest.mark.django_db
def test_create_order_success(user, product):
    client = APIClient()
    client.force_authenticate(user=user)

    # Set initial product stock
    product.stock = 10
    product.price = 100  # Assuming each product costs 100
    product.save()

    # Prepare order data with product and quantity
    data = {
        'products': [
            {'product_id': product.id, 'quantity': 2}
        ],
        'total_amount': 200  # Update to 200 as the expected total amount
    }

    response = client.post('/api/orders/', data, format='json')

    # Assertions
    assert response.status_code == 201
    assert Order.objects.count() == 1
    assert Order.objects.first().total_amount == 200
    assert OrderProduct.objects.filter(order=Order.objects.first(), product=product).exists()

    # Check that stock was reduced correctly
    product.refresh_from_db()
    assert product.stock == 8  # Stock reduced by 2
    
    
    
@pytest.mark.django_db
def test_create_order_insufficient_stock(user, product):
    client = APIClient()
    client.force_authenticate(user=user)

    # Set product stock lower than the requested order quantity
    product.stock = 1
    product.save()

    # Prepare order data with quantity exceeding stock
    data = {
        'products': [
            {'product_id': product.id, 'quantity': 2}
        ],
        'total_amount': 100
    }

    response = client.post('/api/orders/', data, format='json')

    # Assert that the API returns 400 for insufficient stock
    assert response.status_code == 400
    assert response.data['detail'] == f'Insufficient stock for product {product.name}'

    # Ensure that no order was created
    assert Order.objects.count() == 0