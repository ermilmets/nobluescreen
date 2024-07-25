from django.utils.deprecation import MiddlewareMixin


class CurrencyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'currency' not in request.session:
            request.session['currency'] = 'EUR'


