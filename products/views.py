from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    ListView,
    View,
)
from products.models import *
from products.forms import *


class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by = 12
    ordering = ['pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['platform'] = Platform.objects.all()
        context['platforms'] = Platform.objects.filter(slug=self.kwargs.get('platform', ''))
        context['genres'] = Genre.objects.all()
        item_total = 0
        if self.request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=self.request.user)
            user_cart_items = CartItem.objects.filter(cart=user_cart)
            for cart_item in user_cart_items:
                item_total += cart_item.quantity
        else:
            cart = self.request.session.get('cart', {})
            for item, quantity in cart.items():
                item_total += quantity
        context['item_total'] = item_total
        return context


class ProductDetailView(DetailView, FormView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    form_class = ProductRatingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['platform'] = Platform.objects.all()
        context['average_rating'] = product.average_rating()
        context['product_ratings'] = ProductRating.objects.all()
        context['platforms'] = Platform.objects.filter(name=product.platform.name)
        context['has_ordered'] = False
        if self.request.user.is_authenticated:
            try:
                context['user_rating'] = ProductRating.objects.get(product=product, user=self.request.user)
            except ProductRating.DoesNotExist:
                context['user_rating'] = None
        item_total = 0
        if self.request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=self.request.user)
            user_cart_items = CartItem.objects.filter(cart=user_cart)
            for cart_item in user_cart_items:
                item_total += cart_item.quantity
        else:
            cart = self.request.session.get('cart', {})
            for item, quantity in cart.items():
                item_total += quantity
        context['item_total'] = item_total
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
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
        return redirect('product_detail', pk=self.get_object().id)

    def form_invalid(self, form):
        messages.error(self.request, 'Error, when leaving a feedback, '
                                     'please fill out both commentfield and ratingfield!')
        return redirect('product_detail', pk=self.get_object().id)


class GamePlatformView(ListView):
    model = Product
    template_name = 'game_platform.html'
    context_object_name = 'products'

    def get_queryset(self):
        selected_platform = self.kwargs.get('platform', 'PS5')
        platform_object = get_object_or_404(Platform, slug=selected_platform)
        return Product.objects.filter(platform=platform_object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platform'] = Platform.objects.all()
        context['selected_platform'] = self.kwargs.get('platform')
        context['platforms'] = Platform.objects.filter(slug=self.kwargs.get('platform'))
        context['product_ratings'] = ProductRating.objects.all()
        item_total = 0
        if self.request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=self.request.user)
            user_cart_items = CartItem.objects.filter(cart=user_cart)
            for cart_item in user_cart_items:
                item_total += cart_item.quantity
        else:
            cart = self.request.session.get('cart', {})
            for item, quantity in cart.items():
                item_total += quantity
        context['item_total'] = item_total

        return context


class AddToCartView(View):
    def post(self, request, product_id):
        quantity = int(request.POST.get('quantity', 1))
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=product_id)
            user_cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()
        product_id = str(product_id)
        cart = request.session.get('cart', {})
        if cart.get(product_id):
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        request.session['cart'] = cart
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Item added to cart'}, status=200)
        return redirect('cart_detail')


class RemoveFromCartView(View):
    def post(self, request, product_id):
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=product_id)
            user_cart = get_object_or_404(Cart, user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
            cart_item.quantity -= quantity
            if cart_item.quantity <= 0:
                cart_item.delete()
                if not user_cart:
                    del cart
            else:
                cart_item.save()
        product_id = str(product_id)
        cart = request.session.get('cart', {})
        if cart.get(product_id):
            cart[product_id] -= quantity
            if cart[product_id] <= 0:
                del cart[product_id]
        request.session['cart'] = cart
        return redirect('cart_detail')


class CartDetailView(DetailView):
    template_name = 'cart_detail.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=request.user)
            user_cart_items = CartItem.objects.filter(cart=user_cart)
            total = 0
            item_total = 0
            cart_items = []
            cart = request.session.get('cart', {})
            if user_cart_items:
                for cart_item in user_cart_items:
                    cart = {cart_item.product_id: cart_item.quantity}
                    product = get_object_or_404(Product, pk=cart_item.product.id)
                    total += cart_item.product.price * cart_item.quantity
                    item_total += 1 * cart_item.quantity
                    cart_items.append({
                        'product': product,
                        'quantity': cart_item.quantity,
                        'total_price': cart_item.product.price * cart_item.quantity,
                    })
            else:
                for product_id, quantity in cart.items():
                    product = get_object_or_404(Product, pk=product_id)
                    total += product.price * quantity
                    item_total += 1 * quantity
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'total_price': product.price * quantity,
                    })
            cart_items.sort(key=lambda x: x['quantity'], reverse=True)
        else:
            cart = request.session.get('cart', {})
            total = 0
            item_total = 0
            cart_items = []
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, pk=product_id)
                total += product.price * quantity
                item_total += 1 * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': product.price * quantity,
                })
            cart_items.sort(key=lambda x: x['quantity'], reverse=True)
        return render(request, self.template_name, {'cart_items': cart_items, 'total': total,
                                                    'item_total': item_total, 'platform': Platform.objects.all()})

    def post(self, request):
        cart = request.session.get('cart', {})
        product_id = str(request.POST.get('product_id', ''))
        quantity = int(request.POST.get('quantity', '1'))
        if cart.get(product_id):
            cart[product_id] += quantity
            if cart[product_id] <= 0:
                del cart[product_id]
        request.session['cart'] = cart
        return redirect('cart_detail')


class CheckoutView(View):
    template_name = 'checkout.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        user_cart_items = CartItem.objects.filter(cart=user_cart)
        # user_cart_items = get_object_or_404(CartItem, cart=user_cart)
        total = 0
        item_total = 0
        cart_items = []
        # cart = request.session.get('cart', {})
        # total = sum(item.product.price * item.quantity for item in cart_items)
        if user_cart_items:
            for cart_item in user_cart_items:
                # cart = {cart_item.product_id: cart_item.quantity}
                product = get_object_or_404(Product, pk=cart_item.product.id)
                total += cart_item.product.price * cart_item.quantity
                item_total += 1 * cart_item.quantity
                cart_items.append({
                    'product': product,
                    'quantity': cart_item.quantity,
                    'total_price': cart_item.product.price * cart_item.quantity,
                })
        else:
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, pk=product_id)
                total += product.price * quantity
                item_total += 1 * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': product.price*quantity,
                })
        form = CheckoutForm(request.POST or None)
        return render(request, self.template_name, {'form': form, 'cart_items': cart_items,
                                                    'total': total, 'item_total': item_total,
                                                    'platform': Platform.objects.all()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            cart = request.session.get('cart', {})
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            order = Order.objects.create(user=request.user, first_name=first_name,
                                         last_name=last_name, email=email,
                                         phone=phone, address=address, city=city, order_complete=True)
            if cart:
                user_cart = get_object_or_404(Cart, user=request.user)
                for product_id, quantity in cart.items():
                    product = get_object_or_404(Product, pk=product_id)
                    OrderItem.objects.create(user=request.user, order=order,
                                             product=product, quantity=quantity)
                del request.session['cart']
                user_cart.cartitem_set.all().delete()
            return redirect('checkout_success')
        return render(request, self.template_name, {'form': form})


class AboutUsView(ListView):
    model = Product
    template_name = 'aboutus.html'
    context_object_name = 'products'
    # ordering = ['pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['platform'] = Platform.objects.all()
        context['platforms'] = Platform.objects.filter(slug=self.kwargs.get('platform', ''))
        context['genres'] = Genre.objects.all()
        item_total = 0
        if self.request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=self.request.user)
            user_cart_items = CartItem.objects.filter(cart=user_cart)
            for cart_item in user_cart_items:
                item_total += cart_item.quantity
        else:
            cart = self.request.session.get('cart', {})
            for item, quantity in cart.items():
                item_total += quantity
        context['item_total'] = item_total
        return context


class ContactUsView(ListView):
    model = Product
    template_name = 'contactus.html'
    context_object_name = 'products'
    # ordering = ['pk']

    def item_total_method(self, request, *args, **kwargs):
        item_total = 0
        if self.request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=self.request.user)
            user_cart_items = CartItem.objects.filter(cart=user_cart)
            for cart_item in user_cart_items:
                item_total += cart_item.quantity
        else:
            cart = self.request.session.get('cart', {})
            for item, quantity in cart.items():
                item_total += quantity
        return item_total

    def get(self, request, *args, **kwargs):
        form = ContactUsForm(request.POST or None)
        return render(request, self.template_name, {'form': form, 'platform': Platform.objects.all(),
                                                    'item_total': self.item_total_method(request, *args, **kwargs)})

    def post(self, request, *args, **kwargs):
        form = ContactUsForm(request.POST or None)
        if form.is_valid():
            return redirect('message_sent')


class ContactUsSent(ListView):
    template_name = 'contactus_sent.html'

    def item_total_method(self, request, *args, **kwargs):
        item_total = 0
        if self.request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=self.request.user)
            user_cart_items = CartItem.objects.filter(cart=user_cart)
            for cart_item in user_cart_items:
                item_total += cart_item.quantity
        else:
            cart = self.request.session.get('cart', {})
            for item, quantity in cart.items():
                item_total += quantity
        return item_total

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'platform': Platform.objects.all(),
                                                    'item_total': self.item_total_method(request, *args, **kwargs)})


class CustomLoginView(ListView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platform'] = Platform.objects.all()
        return context


class CheckoutSuccessView(ListView):
    template_name = 'checkout_success.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'platform': Platform.objects.all()})


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
    success_url = reverse_lazy('home')  # success_url = '/'
