from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views import generic
from .models import *

# Create your views here.

def index(request):
    return render(request, "first_page_deli/index.html")
    
def shelf_detail_view(request, shelf_name):

    model_map = {
        "HotCase": HotCase,
        "SandwichEndI": SandwichEndI,
        "SandwichEndII": SandwichEndII,
        "ServiceCaseMeats": ServiceCaseMeats,
        "ServiceCaseSalads": ServiceCaseSalads,
        "PackedMeatI": PackedMeatI,
        "PackedMeatII": PackedMeatII,
        "SaladsEnd": SaladsEnd,
        "PizzaAndSalads": PizzaAndSalads,
        "SoupsAndMeals": SoupsAndMeals,
        "EntertainmentEnd": EntertainmentEnd,
        "Pasta": Pasta,
        "Dips": Dips,
        "CheeseBoard": CheeseBoard,
        "Pizza": Pizza,
    }

    model = model_map.get(shelf_name)
    if not model:
        return render(request, 'first_page_deli/404.html')

    items = model.objects.all().order_by('item_name')

    # Render the template with the items
    return render(request, 'first_page_deli/shelf_detail.html', {
        'items': items,
        'shelf_name': shelf_name
    })

def on_sale_view(request, shelf_name):
    model_map = {
        "OnSaleMeats": OnSaleMeats,
        "OnSaleSalads": OnSaleSalads,
    }

    model = model_map.get(shelf_name)
    if not model:
        return render(request, 'first_page_deli/404.html')

    items = model.objects.all().first()  # Get the first (and probably only) instance
    if shelf_name == "OnSaleMeats":
        items = items.on_sale_meats.all().order_by('item_name')
    elif shelf_name == "OnSaleSalads":
        items = items.on_sale_salads.all().order_by('item_name')

    return render(request, 'first_page_deli/OnSale.html', {
        'items': items,
        'shelf_name': shelf_name
    })

def place_order(request, product_id):
    product = get_object_or_404(Pizza, id = product_id)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        total_price = product.price * quantity
        order = OrderPizza.objects.create(product_ordered = product, quantity_ordered=quantity, total_price=total_price)
        return redirect('payment_placeholder', order_id = order.id)
    return render(request, 'place_order.html', {
        'product': product
    })

# views.py

def payment_placeholder(request, order_id):
    order = get_object_or_404(OrderPizza, id=order_id)
    
    # For now, just confirm the order without processing payment
    context = {
        'order': order,
        'message': 'Payment functionality will be added soon. Your order has been placed successfully!',
    }
    return render(request, 'first_page_deli/payment_placeholder.html', context)

# views.py

def build_your_own_pizza(request):
    crusts = crust_choices
    sizes = size_choices
    sauces = sauce_choices
    meats = PizzaMeat.objects.all()
    cheeses = cheese_choices
    toppings = PizzaToppings.objects.all()

    context = {
        'crusts': crusts,
        'sizes': sizes,
        'sauces': sauces,
        'meats': meats,
        'cheeses': cheeses,
        'toppings': toppings,
    }

    if request.method == "POST":
        # Get pizza details from form submission
        crust = request.POST.get('crust')
        size = request.POST.get('size')
        sauce = request.POST.get('sauce')
        meats = request.POST.getlist('meats')
        cheeses = request.POST.getlist('cheese')
        toppings = request.POST.getlist('toppings')
        quantity = int(request.POST.get('quantity', 1))

        # Get customer information from form submission
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        # Calculate the base price of the pizza
        base_price = 17.99  # You can adjust this or calculate based on selections
        total_price = base_price * quantity

        # Create a new OrderPizza instance and set fields
        order = OrderPizza.objects.create(
            crust=crust,
            size=size,
            sauce=sauce,
            cheese=','.join(cheeses),
            price=base_price,
            quantity_ordered=quantity,
            total_price=total_price,
            customer_name=customer_name,
            phone_number=phone_number,
            email=email
        )

        # Set many-to-many relationships
        order.meat.set(meats)
        order.toppings.set(toppings)

        # Redirect to the payment page or another relevant page
        return redirect('payment_placeholder', order_id=order.id)

    return render(request, 'first_page_deli/BYOPizza.html', context)

def search_view(request):
    query = request.GET.get('q')  # Get the search query from the request
    results = []

    if query:
        # List of models to search across
        models_to_search = [
            Pizza,
        ]

        # Search each model for the query in relevant fields
        for model in models_to_search:
            model_results = model.objects.filter(
                Q(item_name__icontains=query) | Q(crust__icontains=query) | Q(cheese__icontains=query) 
                | Q(sauce__icontains=query) 
            )
            results.extend(model_results)

    return render(request, 'first_page_deli/search_results.html', {
        'query': query,
        'results': results
    })
