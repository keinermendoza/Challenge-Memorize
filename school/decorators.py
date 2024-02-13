from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def custom_login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
   
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        def decorated_add_message(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to access this page.")
            return actual_decorator(function)(request, *args, **kwargs)
        return decorated_add_message
    return actual_decorator