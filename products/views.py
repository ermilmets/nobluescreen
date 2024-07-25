from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
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
        context['platform'] = Platform.objects.all()
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
        return redirect('product_detail', pk=self.get_object().id)  # product_id=self.get_object().id


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
        context['platform'] = Platform.objects.all()
        context['selected_platform'] = self.kwargs.get('platform')  # self.platform  context['platform']
        context['platforms'] = Platform.objects.filter(slug=self.kwargs.get('platform'))
        context['product_ratings'] = ProductRating.objects.all()

        return context


class AddToCartView(View):
    # @method_decorator(login_required)  # 'next'  (redirect_field_name='cart_detail')
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
        # del request.session['cart']
        product_id = str(product_id)
        cart = request.session.get('cart', {})
        if cart.get(product_id):
            cart[product_id] += quantity  # 1
        else:
            cart[product_id] = quantity  # 1
        request.session['cart'] = cart
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Item added to cart'}, status=200)
        return redirect('cart_detail')  # (, pk=cart_item.pk)


class RemoveFromCartView(View):
    # @method_decorator(login_required)
    def post(self, request, product_id):  # or post
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=product_id)
            # user_cart, created = Cart.objects.get_or_create(user=request.user)
            user_cart = get_object_or_404(Cart, user=request.user)
            # user_cart.delete()
            cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)  # for safety, needed
            # cart_item= get_object_or_404(CartItem, cart=user_cart, product=product)
            if cart_item.quantity == 1:
                cart_item.delete()
            else:
                cart_item.quantity -= 1
                cart_item.save()
        # product = get_object_or_404(Product, pk=product_id)
        product_id = str(product_id)
        cart = request.session.get('cart', {})
        if cart.get(product_id):
            if cart.get(product_id) == 1:
                del cart[product_id]
            else:
                cart[product_id] -= 1
        request.session['cart'] = cart
        return redirect('cart_detail')


class CartDetailView(DetailView):  # LoginRequiredMixin,
    # model = Product
    template_name = 'cart_detail.html'

    # ordering = ['pk']
    # context_object_name = 'products'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['platform'] = Platform.objects.all()
    #     return context

    # @method_decorator(login_required)  # (redirect_field_name='cart_detail')
    def get(self, request, *args, **kwargs):
        # cart, created = Cart.objects.get_or_create(user=request.user)
        # product = get_object_or_404(Product, pk=kwargs.get('pk'))
        if request.user.is_authenticated:
            # user_cart, created = Cart.objects.get_or_create(user=request.user)
            user_cart = get_object_or_404(Cart, user=request.user)
            user_cart_items = CartItem.objects.filter(cart=user_cart)
            total = 0
            item_total = 0
            cart_items = []
            cart = request.session.get('cart', {})
            # total = sum(item.product.price * item.quantity for item in cart_items)
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
            # request.session['cart'] = cart
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
        return render(request, self.template_name, {'cart_items': cart_items, 'total': total,
                                                    'item_total': item_total, 'platform': Platform.objects.all()})
        # return render(request, self.template_name, {'cart': cart,
        #                                             'cart_total': cart_total, 'item_total': item_total})

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
            # request.session['cart'] = cart
        else:  # in case user cart is empty, overwrite with session cart
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, pk=product_id)
                total += product.price * quantity
                item_total += 1 * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': product.price*quantity,
                })
        # request.session['cart'] = cart
        form = CheckoutForm(request.POST or None)
        return render(request, self.template_name, {'form': form, 'cart_items': cart_items,
                                                    'total': total, 'item_total': item_total,
                                                    'platform': Platform.objects.all()})
        # return render(request, self.template_name, {'form': form,
        #                                             'cart': cart, 'cart_total': cart_total, 'item_total': item_total})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            cart = request.session.get('cart', {})
            # cart = get_object_or_404(Cart, user=request.user)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            order = Order.objects.create(user=request.user, first_name=first_name,
                                         last_name=last_name, email=email,
                                         phone=phone, address=address, city=city, order_complete=True)
            # dummy order processing
            if cart:
                # user_cart = Cart.objects.get(user=request.user)  # get_or_create  user_cart, created
                user_cart = get_object_or_404(Cart, user=request.user)
                # user_cart_items = CartItem.objects.filter(cart=user_cart)
                # user_cart.cartitem_set.all().delete()
                for product_id, quantity in cart.items():
                    product = get_object_or_404(Product, pk=product_id)
                    OrderItem.objects.create(user=request.user, order=order,
                                             product=product, quantity=quantity)
                    # CartItem.objects.create(cart=user_cart, product=product, quantity=quantity)
                # for item in user_cart.cartitem_set.all():
                    # CartItem.objects.create(cart=user_cart, product=item.product, quantity=item.quantity)
                # for item in user_cart.cartitem_set.all():    # user_cart.cartitem_set.all():
                #     OrderItem.objects.create(user=request.user, order=order,
                #                              product=item.product, quantity=item.quantity)
                del request.session['cart']
                # user_cart.items.clear()
                user_cart.cartitem_set.all().delete()  # clearing the user_cart
                # user_cart.products.clear()
            return redirect('checkout_success')
        return render(request, self.template_name, {'form': form})


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
