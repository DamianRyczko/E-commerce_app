from django.core.exceptions import PermissionDenied
from functools import wraps

from django.shortcuts import redirect

def allowed_roles(allowed_groups=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            # Check if user belongs to any of the required groups
            user_groups = request.user.groups.values_list('name', flat=True)
            if any(group in user_groups for group in allowed_groups):
                return view_func(request, *args, **kwargs)

            raise PermissionDenied

        return _wrapped_view

    return decorator