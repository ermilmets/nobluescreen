from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView, ListView, View
from products.models import *
from products.forms import *


class HomePageView(ListView):  # TemplateView
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    ordering = ['pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['platform'] = Platform.objects.all()
        context['genres'] = Genre.objects.all()
        return context


class ProductDetailView(DetailView, FormView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    form_class = ProductRatingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['average_rating'] = product.average_rating()
        context['product_ratings'] = ProductRating.objects.all()
        # context['platform'] = Platform.objects.all()
        if self.request.user.is_authenticated:
            try:
                context['user_rating'] = ProductRating.objects.get(product=product, user=self.request.user)
            except ProductRating.DoesNotExist:
                context['user_rating'] = None
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # reverse_lazy('login')
        user_feedback = self.get_object()
        form = self.get_form()
        if form.is_valid():
            star_rating, created = ProductRating.objects.update_or_create(
                product=user_feedback, user=request.user,
                defaults={'star_rating': form.cleaned_data['star_rating'],
                          'feedback': form.cleaned_data['feedback']})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # form.save()
        return redirect('product_detail', pk=self.get_object().id)   # product_id=self.get_object().id


class GamePlatformView(ListView):  # based on chosen category, shows games only on chosen platform
    model = Product
    template_name = 'game_platform.html'
    context_object_name = 'products'

    def get_queryset(self):
        selected_platform = self.kwargs.get('platform', 'PS5')
        platform_object = get_object_or_404(Platform, slug=selected_platform)
        return Product.objects.filter(platform=platform_object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['platform'] = Platform.objects.all()
        context['platform'] = self.kwargs.get('platform')  # self.platform
        context['product_ratings'] = ProductRating.objects.all()

        return context


class AddToCartView(View):
    @method_decorator(login_required(redirect_field_name='cart_detail'))  # 'next'
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart_detail')   # (, pk=cart_item.pk)


class RemoveFromCartView(View):
    @method_decorator(login_required)
    def post(self, request, product_id):  # or post
        product = get_object_or_404(Product, pk=product_id)
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)  # cart__user=request.user

        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        return redirect('cart_detail')


class CartDetailView(DetailView):  # LoginRequiredMixin,
    # model = Cart
    template_name = 'cart_detail.html'
    # context_object_name = 'cart'

    @method_decorator(login_required(redirect_field_name='cart_detail'))
    def get(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'cart': cart})


class CheckoutView(View):
    template_name = 'checkout.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST or None)
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            # cart = Cart.objects.get_or_create(user=request.user)
            cart = get_object_or_404(Cart, user=request.user)
            # dummy order processing
            cart.products.clear()
            return redirect('checkout_success')


class CheckoutSuccessView(View):
    template_name = 'checkout_success.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


# class CartItemView(ListView):
#     model = Product
#     template_name = 'cart_detail.html'
#     context_object_name = 'products'


class CreateFeedbackView(CreateView, LoginRequiredMixin):
    model = ProductRating
    template_name = 'product_ratings/create_feedback.html'
    context_object_name = 'ratings'
    success_url = reverse_lazy('home')  # necessary?
    # django class based views override
    # Product.objects.update(total_rating=69)

    def form_valid(self, form):
        form.instance.author = self.request.user


class UpdateFeedbackView(UpdateView, LoginRequiredMixin):
    model = ProductRating
    template_name = 'product_ratings/create_feedback.html'
    context_object_name = 'ratings'
    success_url = reverse_lazy('home')


class DeleteFeedbackView(DeleteView, LoginRequiredMixin):
    model = ProductRating
    template_name = 'product_ratings/confirm_delete_feedback.html'
    context_object_name = 'ratings'
    success_url = reverse_lazy('home')   # success_url = '/'







