from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from website.api.serialization.product_serializer import ProductSerializer
from website.models import Products
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def product_list(request):
    products = Products.objects.all()
    serialized = ProductSerializer(products, many=True)
    return Response(serialized.data)

@api_view(['POST'])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def product_update(request, pk):
    try:
        product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def product_delete(request, pk):
    try:
        product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        
        cart = request.session.get('cart', {})
        
        if product_id and action:
            if action == 'add':
                cart[product_id] += 1
            elif action == 'remove':
                cart[product_id] -= 1
                if cart[product_id] <= 0:
                    del cart[product_id]
            request.session['cart'] = cart
    
    return redirect('cart')