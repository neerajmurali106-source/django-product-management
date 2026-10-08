from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Category, Product


@login_required
def dashboard(request):
    total_products = Product.objects.count()

    active_products = Product.objects.filter(
        status="active"
    ).count()

    inactive_products = Product.objects.filter(
        status="inactive"
    ).count()

    low_stock_products = Product.objects.filter(
        stock__lte=5
    ).count()

    context = {
        "total_products": total_products,
        "active_products": active_products,
        "inactive_products": inactive_products,
        "low_stock_products": low_stock_products,
    }

    return render(
        request,
        "products/dashboard.html",
        context
    )


@login_required
def product_list(request):
    products = Product.objects.select_related("category").all()

    search = request.GET.get("search", "").strip()
    category_id = request.GET.get("category", "")
    status = request.GET.get("status", "")

    if search:
        products = products.filter(
            Q(name__icontains=search)
        )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    if status:
        products = products.filter(
            status=status
        )

    categories = Category.objects.all()

    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "search": search,
        "selected_category": category_id,
        "selected_status": status,
    }

    return render(
        request,
        "products/product_list.html",
        context
    )

@login_required
def product_form(request, pk=None):

    if pk:
        product = get_object_or_404(Product, pk=pk)
        page_title = "Edit Product"
    else:
        product = None
        page_title = "Add Product"

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()

            return redirect("product_list")

    else:

        form = ProductForm(instance=product)

    context = {
        "form": form,
        "page_title": page_title,
        "product": product,
    }

    return render(
        request,
        "products/product_form.html",
        context
    )

@login_required
def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        pk=pk
    )

    return render(
        request,
        "products/product_detail.html",
        {"product": product}
    )


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(
        request,
        "products/product_confirm_delete.html",
        {"product": product}
    )