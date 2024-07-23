from django.urls import path, include
from .views import *
from . import views
from django.urls import URLPattern, URLResolver
from django.urls import path, include

def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    for entry in lis:
        if isinstance(entry, URLPattern):
            acc.append(entry.pattern.regex.pattern)
        elif isinstance(entry, URLResolver):
            list_urls(entry.url_patterns, acc)
    return acc
urlpatterns = [
    path("", HomePageView.as_view(), name='home'),   # has to be int:pk
    path("product/<int:pk>", ProductDetailView.as_view(), name='product_detail'),
    path("platform/<slug:platform>", GamePlatformView.as_view(), name='gameplatform'),
    path("cart/add/<int:product_id>", AddToCartView.as_view(), name='add_to_cart'),
    path("cart/remove/<int:product_id>", RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path("checkout/", CheckoutView.as_view(), name='checkout'),
    path("checkout/success/", CheckoutSuccessView.as_view(), name='checkout_success'),
    path("rating", CreateFeedbackView.as_view(), name='rating'),
    path("rating/update", UpdateFeedbackView.as_view(), name='update_rating'),
    path("rating/confim_delete", DeleteFeedbackView.as_view(), name='confirm_delete'),
    path('section2/', views.section2, name='section2'),
    path('section3/', views.section3, name='section3'),
    path('section4/', views.section4, name='section4'),
    path('section5/', views.section5, name='section5'),
    path('section6/', views.section6, name='section6'),
    path('section7/', views.section7, name='section7'),
    path('section8/', views.section8, name='section8'),
    path('section9/', views.section9, name='section9'),
]






