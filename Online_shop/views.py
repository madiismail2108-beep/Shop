from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView, TemplateView, FormView
)
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.core.mail import send_mail
from django.conf import settings

from .models import Category, Product
from .forms import CategoryForm, ProductForm, ContactForm

class HomeView(TemplateView):
    template_name = 'shop/home.html'

class CategoryListView(ListView):
    model = Category
    template_name = 'store/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'store/form.html'
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.annotate(
            avg_rating=Coalesce(Avg('reviews__rating'), 0.0)
        ).order_by('-avg_rating', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        overall = Product.objects.aggregate(overall_avg=Avg('reviews__rating'))
        context['overall_avg'] = round(overall['overall_avg'] or 0.0, 2)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product-detail.html'
    pk_url_kwarg = 'product_id'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/form.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.object.id})

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/form.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.object.id})

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')

class ContactView(FormView):
    template_name = 'store/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        cd = form.cleaned_data
        send_mail(
            subject=f"[Contact] {cd['subject']}",
            message=f"From: {cd['name']} <{cd['email']}>\n\n{cd['message']}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'store/contact_success.html'
