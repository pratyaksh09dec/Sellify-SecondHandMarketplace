from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import get_profile
from ai_engine.image_recognition import detect_category
from ai_engine.price_predictor import predict_price

from .forms import PhotoForm, ProductEditForm, ProductForm
from .models import CATEGORY_CHOICES, CONDITION_CHOICES, Product


def home(request):
    """Browse page with search and filters."""
    products = Product.objects.filter(is_sold=False)

    q = request.GET.get("q", "")
    category = request.GET.get("category", "")
    condition = request.GET.get("condition", "")
    brand = request.GET.get("brand", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")

    if q:
        products = products.filter(name__icontains=q)
    if category:
        products = products.filter(category=category)
    if condition:
        products = products.filter(condition=condition)
    if brand:
        products = products.filter(brand__icontains=brand)
    if min_price.isdigit():
        products = products.filter(expected_price__gte=int(min_price))
    if max_price.isdigit():
        products = products.filter(expected_price__lte=int(max_price))

    context = {
        "products": products,
        "categories": CATEGORY_CHOICES,
        "conditions": CONDITION_CHOICES,
        "f": request.GET,
    }
    return render(request, "marketplace/home.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    seller_profile = get_profile(product.seller)
    return render(request, "marketplace/product_detail.html",
                  {"product": product, "seller_profile": seller_profile})


@login_required
def sell_photo(request):
    if not get_profile(request.user).is_seller:
        messages.warning(request, "Tick 'I want to sell products' in your profile first.")
        return redirect("profile")

    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data["image"]
            saved_path = default_storage.save("products/" + photo.name, photo)

            category, confidence = detect_category(default_storage.path(saved_path))

            request.session["new_image"] = saved_path
            request.session["ai_category"] = category
            request.session["ai_confidence"] = confidence
            return redirect("sell_details")
    else:
        form = PhotoForm()
    return render(request, "marketplace/sell_photo.html", {"form": form})

@login_required
def sell_details(request):
    image_path = request.session.get("new_image")
    if not image_path:
        return redirect("sell_photo")

    ai_category = request.session.get("ai_category")
    ai_confidence = request.session.get("ai_confidence")
    predicted = None

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            predicted = predict_price(data["original_price"], data["age_months"], data["condition"])

            if request.POST.get("action") == "publish":
                product = form.save(commit=False)
                product.seller = request.user
                product.image = image_path
                product.predicted_price = predicted
                product.save()
                for key in ["new_image", "ai_category", "ai_confidence"]:
                    request.session.pop(key, None)
                messages.success(request, "Your listing is live!")
                return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm(initial={"category": ai_category})

    context = {
        "form": form,
        "image_url": default_storage.url(image_path),
        "ai_category": dict(CATEGORY_CHOICES).get(ai_category),
        "ai_confidence": ai_confidence,
        "predicted": predicted,
        "low": round(predicted * 0.9) if predicted else None,
        "high": round(predicted * 1.1) if predicted else None,
    }
    return render(request, "marketplace/sell_details.html", context)

@login_required
def my_listings(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, "marketplace/my_listings.html", {"products": products})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)  # only your own
    if request.method == "POST":
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.predicted_price = predict_price(
                product.original_price, product.age_months, product.condition)
            product.save()
            messages.success(request, "Listing updated.")
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductEditForm(instance=product)
    return render(request, "marketplace/edit_product.html", {"form": form, "product": product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Listing deleted.")
        return redirect("my_listings")
    return render(request, "marketplace/confirm_delete.html", {"product": product})


@login_required
def mark_sold(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.is_sold = True
        product.save()
        messages.success(request, f"'{product.name}' marked as sold.")
    return redirect("my_listings")
