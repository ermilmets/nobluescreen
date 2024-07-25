from django.urls import path, include
from .views import *
from .views import change_currency

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),   # has to be int:pk
    path("product/<int:pk>", ProductDetailView.as_view(), name='product_detail'),
    path("platform/<slug:platform>", GamePlatformView.as_view(), name='gameplatform'),
    path("cart/add/<int:product_id>", AddToCartView.as_view(), name='add_to_cart'),
    path("cart/remove/<int:product_id>", RemoveFromCartView.as_view(), name='remove_from_cart'),
    path("cart/", CartDetailView.as_view(), name='cart_detail'),
    path("checkout/", CheckoutView.as_view(), name='checkout'),
    path("checkout/success/", CheckoutSuccessView.as_view(), name='checkout_success'),
    path("rating", CreateFeedbackView.as_view(), name='rating'),
    path("rating/update", UpdateFeedbackView.as_view(), name='update_rating'),
    path("rating/confim_delete", DeleteFeedbackView.as_view(), name='confirm_delete'),
    path('change_currency/', change_currency, name='change_currency'),

]






