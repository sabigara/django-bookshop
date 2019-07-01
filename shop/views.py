from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import View
from django.shortcuts import render

from .models import Book


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = Book.objects \
                    .select_related('publisher') \
                    .prefetch_related('authors') \
                    .order_by('publish_date')

        keyword = request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(desctiption__icontains=keyword)
            )

        context = {
            'keyword': keyword,
            'book_list': queryset,
        }

        return render(request, 'shop/book_list.html', context)


index = IndexView.as_view()


class DetailView(LoginRequiredMixin, View):
    def get(self, request, book_id, *args, **kwargs):
        book = Book.objects.get(pk=book_id)
        context = {
            'book': book,
            'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, 'shop/book_detail.html', context)


detail = DetailView.as_view()
