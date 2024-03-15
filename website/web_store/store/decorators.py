from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def cookie_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.COOKIES.get('cookieConsent') == 'true':
            # Add an error message
            messages.error(request, "Cookie consent is required to access this page.")
            return redirect('cookie_info')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
