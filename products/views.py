from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView
from products.models import *


class HomePageView(TemplateView):
    model = Product
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category'] = Platform.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class GamePlatformView(TemplateView):  # based on chosen category, shows games only on chosen platform
    template_name = 'game_platform.html'


class CreateFeedbackView(CreateView, LoginRequiredMixin):
    model = ProductRating
    template_name = 'product_ratings/create_feedback.html'
    context_object_name = 'ratings'
    success_url = reverse_lazy('home')  # necessary?
    # django class based views override
    # Product.objects.update(total_rating=69)


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







