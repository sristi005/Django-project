from core.models import Login

def get_logged_in_user(request):
    """Returns the Login object for the current session, or None."""
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return Login.objects.filter(id=user_id).first()


def login_required(view_func):
    from functools import wraps
    from django.shortcuts import redirect
    from django.contrib import messages

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not get_logged_in_user(request):
            messages.error(request, "Please sign in first")
            return redirect('signin_page')
        return view_func(request, *args, **kwargs)
    return wrapper