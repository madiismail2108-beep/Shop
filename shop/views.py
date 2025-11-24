from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.core.paginator import Paginator
from .forms import CategoryForm, ProductForm
from .models import Category,Product,Attribute, AttributeKey, AttributeValue
from django.db.models import Avg
from django.db.models.functions import Coalesce
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories':categories,
        'products':products
    }
    return render(request,'templates/store/index.html',context)

class Index(View):
    def get(self,request,category_slug=None):
        categories = Category.objects.all()
        products = Product.objects.all()
        paginator = Paginator(products,3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            'categories':categories,
            'page_obj':page_obj
        }
        if category_slug:
            products = Product.objects.filter(category__slug = category_slug)
            context = {
                'products':products,
            }
            return render(request,'templates/store/product-list.html',context)

        return render(request,'templates/store/index.html',context)

class ProductDetail(DetailView):
    model = Product
    template_name = 'templates/store/product-detail.html'   
    pk_url_kwarg = 'product_id'

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'store/form.html', {'form': form})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'store/form.html', {'form': form})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/form.html', {'form': form})

def product_list(request):
    products = Product.objects.annotate(
        avg_rating=Coalesce(Avg('reviews__rating'), 0.0)
    ).order_by('-avg_rating', 'name')

    overall = Product.objects.aggregate(overall_avg=Avg('reviews__rating'))
    overall_avg = overall['overall_avg'] or 0.0

    return render(request, 'store/product_list.html', {
        'products': products,
        'overall_avg': round(overall_avg,2),
    })


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    products = Product.objects.annotate(
        avg_rating=Coalesce(Avg('reviews__rating'), 0.0)
    ).order_by('-avg_rating', 'name')  

    context = {
        'products': products,
    }
    return render(request, 'store/product_list.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                subject=f"[Contact] {cd['subject']}",
                message=f"From: {cd['name']} <{cd['email']}>\n\n{cd['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return render(request, 'store/contact_success.html', {'name': cd['name']})
    else:
        form = ContactForm()
    return render(request, 'store/contact.html', {'form': form})

def home(request):
    return render(request, 'shop/home.html')
# Create your views here.

