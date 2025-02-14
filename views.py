from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product

def shop_list(request):
    # Get all products from the database
    product_list = Product.objects.all()
    
    # Paginate the products list, showing 10 products per page
    paginator = Paginator(product_list, 10)
    
    # Get the current page number from the request
    page_number = request.GET.get('page')
    
    # Get the products for the current page
    products = paginator.get_page(page_number)
    
    # Render the 'shop_list.html' template with the paginated products
    return render(request, 'shop_list.html', {'products': products})