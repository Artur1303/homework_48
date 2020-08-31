from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView,View, ListView
from webapp.models import Product, Basket, Orders, ProductOrder
from webapp.forms import ProductForm, OrederForm
from .base_views import SearchView
from django.db import models
from django.db.models import Q, ExpressionWrapper, F, Sum
class IndexView(SearchView):
    model = Product
    template_name = 'index.html'
    ordering = ['category', 'name']
    search_fields = ['name__icontains']
    paginate_by = 2
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)


class ProductView(DetailView):
    model = Product
    template_name = 'product_view.html'

class ProductCreateView(CreateView):
    template_name = 'product_create.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})



class ProductUpdateView(UpdateView):
    template_name = 'product_update.html'
    form_class = ProductForm
    model = Product


    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('index')


class AddProductOnBasket(View):
    def get(self, request, *args, **kwargs):
       self.product=get_object_or_404(Product,pk = self.kwargs['pk'])
       try:
            existed_product = Basket.objects.get(products=self.product)
            if self.product.amount > existed_product.qty:
                existed_product.qty += 1
                self.product.save()
                existed_product.save()
       except ObjectDoesNotExist:
           if self.product.amount > 0:
            Basket.objects.create(products=self.product, qty=1)

       return redirect('index')


class BasketView(ListView):
    model = Basket
    template_name = 'basket_view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['summ'] = 0
        for baket in Basket.objects.all():
            context['summ'] += baket.total()
        context['form'] = OrederForm()

        return context


class BasketDelete(DeleteView):
    model = Basket
    success_url = reverse_lazy('basket_view')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class OrderCreate(View):
    def post(self, request, *args, **kwargs):
        form = OrederForm(data=request.POST)
        if form.is_valid():
            order = Orders.objects.create(**form.cleaned_data)
            for basket in Basket.objects.all():
                ProductOrder.objects.create(order=order, product=basket.products, qty=basket.qty)
                product = Product.objects.get(pk=basket.products.pk)
                product.amount -= basket.qty
            Basket.objects.all().delete()
            return redirect('index')

        else:
            basket = Basket.objects.all()
            context = {'basket_list': basket, 'form': form }
            return render(request, 'basket_view.html', context)