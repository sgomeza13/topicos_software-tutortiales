from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.shortcuts import render, redirect

# Create your views here.
def homePageView(request):
    return HttpResponse("aaaaaaaaaaaaa")

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "This is an about page ...",
        "author": "Developed by: Your Name",
        })

        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        "phone_number": "+1 1013443765",
        "email": "onlinestore@eafit.edu.co",
        "address": "9049 Foster Ave. Maspeth, NY 11378"        
        })

        return context
    
class Product:
    products = [
    {"id":"1", "name":"TV", "description":"Best TV", "price":600},
    {"id":"2", "name":"iPhone", "description":"Best iPhone", "price":999},
    {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price":50},
    {"id":"4", "name":"Glasses", "description":"Best Glasses", "price":120}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)
    
class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id)-1]
        except:
            return HttpResponseRedirect("/")
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        
        return render(request, self.template_name, viewData)
        
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data['price']
        if (price <= 0):
            raise forms.ValidationError("El precio debe ser mayor a cero")
        return price
    

class ProductCreateView(View):
    template_name = 'products/create.html'
    created_product = 'products/created.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    def post(self, request):
        form = ProductForm(request.POST)
        viewData = {}
        viewData["form"] = form.data
        if form.is_valid():
            return render(request,self.created_product,viewData)
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)