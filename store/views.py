from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import status

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")
        return super().post(request, *args, **kwargs)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        products = request.data.get('products', [])
        total_amount = request.data.get('total_amount', 0)

        for item in products:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)

            try:
                product = Product.objects.get(id=product_id)
                if product.stock < quantity:
                    return Response({'detail': f'Insufficient stock for product {product.name}'}, status=400)

            except Product.DoesNotExist:
                return Response({'detail': f'Product with id {product_id} not found'}, status=404)

        # Assuming order creation logic is here
        order = Order.objects.create(user=user, total_amount=total_amount)
        for item in products:
            product = Product.objects.get(id=item.get('product_id'))
            OrderProduct.objects.create(order=order, product=product, quantity=item.get('quantity', 1))
            product.stock -= item.get('quantity', 1)
            product.save()

        return Response({'message': 'Order created successfully', 'order_id': order.id}, status=201)