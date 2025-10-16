from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
from django.shortcuts import render
from .models import Product, Category  # assuming you have a Category model

def product_list(request):
    query = request.GET.get('q', '')  # search keyword
    category_id = request.GET.get('category', '')  # category filter

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)  # search by product name

    if category_id:
        products = products.filter(category__id=category_id)  # filter by category

    categories = Category.objects.all()  # to populate dropdown

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id
    })

def product_detail(request, id):  # <-- must match 'id' in urls.py
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})
