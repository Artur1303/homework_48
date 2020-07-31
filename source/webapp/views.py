from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.utils.timezone import make_naive

from webapp.models import Product
from webapp.forms import ProductForm


def index_view(request):
    data = Product.objects.order_by('category', 'name')
    return render(request, 'index.html', context={
        'products': data
    })


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_view.html', context)


def product_create_view(request):
    if request.method == "GET":
        return render(request, 'product_create.html', context={
            'form': ProductForm()
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            # product = Product.objects.create(**form.cleaned_data)
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'],
                price=form.cleaned_data['price']
            )
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'product_create.html', context={
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        form = ProductForm(initial={
            'title': product.title,
            'text': product.text,
            'author': product.author,
            'status': product.status,
            # форматирование перед выводом для DateTime.
            'publish_at': make_naive(product.publish_at)\
                .strftime(BROWSER_DATETIME_FORMAT)
            # для дат выглядит просто как:
            # 'publish_at': product.publish_at
        })
        return render(request, 'product_update.html', context={
            'form': form,
            'product': product
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            # product.objects.filter(pk=pk).update(**form.cleaned_data)
            product.title = form.cleaned_data['title']
            product.text = form.cleaned_data['text']
            product.author = form.cleaned_data['author']
            product.status = form.cleaned_data['status']
            product.publish_at = form.cleaned_data['publish_at']
            product.save()
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'product_update.html', context={
                'product': product,
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'product_delete.html', context={'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
