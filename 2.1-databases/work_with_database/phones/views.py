from django.shortcuts import render, redirect, get_object_or_404

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_parameter = request.GET.get("sort")
    sort_parameters ={
        "name": "name",
        "min_price": "price",
        "max_price": "-price",
    }
    sort_parameter = sort_parameters.get(sort_parameter)
    if sort_parameter is None:
        phones = Phone.objects.all()
    else:
        phones = Phone.objects.all().order_by(sort_parameter)
    context = {"phones": phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = get_object_or_404(Phone, slug=slug)
    context = {"phone": phone}
    return render(request, template, context)

