from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView, FormView, ListView
from products.models import *
from django.utils.decorators import method_decorator
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
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            star_rating, created = ProductRating.objects.update_or_create(
                product=self.object, user=request.user,
                defaults={'star_rating': form.cleaned_data['star_rating'],
                          'feedback': form.cleaned_data['feedback']})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # form.save()
        return redirect('product_detail', pk=self.object.id)   # product_id=self.get_object().id


class GamePlatformView(ListView):  # based on chosen category, shows games only on chosen platform
    model = Product
    template_name = 'game_platform.html'
    context_object_name = 'products'

    def get_queryset(self):
        platform = self.kwargs['platform']
        self.platform = get_object_or_404(Platform, slug=platform)
        return Product.objects.filter(platform=self.platform)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['platform'] = Platform.objects.all()
        context['platform'] = self.platform
        context['product_ratings'] = ProductRating.objects.all()

        return context


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







