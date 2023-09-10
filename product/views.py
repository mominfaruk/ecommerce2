from django.shortcuts import render,redirect
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    product_types=ProductType.objects.all()
    products=Product.objects.all()
    context={'product_types':product_types,'products':products}
    return render(request, 'home.html',context)

@api_view(['GET'])
def load_cart_items(request):
    user = request.user
    
    if not user.is_authenticated:
        return Response({"error": "You must be logged in to add to cart."})
    try:
        # Assuming that a user has one cart
        cart = Cart.objects.get(user=user,completed=False)
    except Cart.DoesNotExist:
        return JsonResponse({'cart': []})

    cart_items = CartItem.objects.filter(cart=cart, cart__completed=False)
    cart_items_data = [
        {
            'id': item.product.id,
            'name': item.product.name,
            'price': str(item.product.price),
            'count': item.quantity,
        }
        for item in cart_items
    ]
    return JsonResponse({'cart': cart_items_data})

@api_view(['POST'])
def add_to_cart(request):
    user = request.user
    #check user is valid
    if not user.is_authenticated:
        return Response({"error": "You must be logged in to add to cart."})
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    #if user cart is completed, create a new cart
    try:
        # Assuming that a user has one cart
        cart = Cart.objects.get(user=user, completed=False)
    except Cart.DoesNotExist:
        # If the user does not have a cart, create one
        cart = Cart.objects.create(user=user)
    
    product = Product.objects.get(id=product_id)
    #if product exists in cart, update quantity
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += quantity
        cart_item.save()
        return Response({"detail": "Item added to cart."})
    except CartItem.DoesNotExist:
        pass

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
        defaults={'quantity': quantity},
    )
    # If the cart item already exists, increment the quantity
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return Response({"detail": "Item added to cart."})

@api_view(['POST'])
def update_cart(request):
    print("This is from update")
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "You must be logged in to upadte to cart."})
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    try:
        # Assuming that a user has one cart
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.get(product_id=product_id, cart=cart)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        return Response({"detail": "Cart updated successfully."})
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({"error": "Cart or cart item does not exist."})

@api_view(['POST'])
def remove_from_cart(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "You must be logged in to delete to cart."})
    product_id = request.data.get('product_id')
    try:
        # Assuming that a user has one cart
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.get(product_id=product_id, cart=cart)
        cart_item.delete()
        return Response({"detail": "Item removed from cart."})
    except:
        return Response({"error": "Cart or cart item does not exist."})

@login_required
def checkout_page(request):
    user = request.user
    print(f"Debug: User is {user}")
    if not user.is_authenticated:
        return redirect('login')
    try:
        cart = Cart.objects.get(user=user, completed=False)
    except Cart.DoesNotExist:
        cart = None
    
    if cart is None:
        context = {'error_message': 'Your cart is empty'}
        return render(request, 'checkout.html', context=context)
    
    cart_items = CartItem.objects.filter(cart=cart)
    cart_subtotal = sum([item.product.price * item.quantity for item in cart_items])
    cart_quantity = sum([item.quantity for item in cart_items]) 
    print(f"Debug: Cart items are {cart_items}")
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        if len(cart_items) == 0:
            context = {'message': 'Your cart is empty'}
            return render(request, 'checkout.html', context=context)
        
        if name and phone_number and address and city:
            order = Order.objects.create(
                user=user,
                cart=cart,
                quantity=cart_quantity,
                total_amount=cart_subtotal,
            )
            OrderUserInfo.objects.create(
                user=user,
                order=order,
                name=name,
                phone=phone_number,
                address=address,
                city=city,
            )
            cart.completed = True
            cart.save()
        else:
            context = {'message': 'Please fill in all the fields'}
            return render(request, 'checkout.html', context=context)
        return redirect('/home')
   
    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
    }
    
    return render(request, 'checkout.html', context=context)

