from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, CustomerForm, LoginForm


from .factory import auth_facade_instance

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():

            user_data = {
                'username': user_form.cleaned_data.get('username'),
                'first_name': user_form.cleaned_data.get('first_name'),
                'last_name': user_form.cleaned_data.get('last_name'),
                'email': user_form.cleaned_data.get('email'),
                'password': user_form.cleaned_data.get('password1'),

            }


            customer_data = customer_form.cleaned_data

            try:
                user = auth_facade_instance.register(
                    user_form_data=user_data,
                    customer_form_data=customer_data
                )
                messages.success(request, f"Account created for {user.username}!")
                return redirect("login")

            except TypeError as e:
                messages.error(request, f"System error (fields mismatch): {e}")
            except Exception as e:
                messages.error(request, f"Registration failed: {e}")

    else:
        user_form = UserRegistrationForm()
        customer_form = CustomerForm()

    context = {
        "user_form": user_form,
        "customer_form": customer_form
    }
    return render(request, "user_login/register.html", context)


def login(request):
    if request.method == "POST":
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()

            auth_facade_instance.login(request, user)

            redirect_path = auth_facade_instance.get_redirect_url(user)

            messages.success(request, f"Login successful for {user.username}!")
            return redirect(redirect_path)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        login_form = LoginForm()

    context = {
        "login_form": login_form
    }
    return render(request, "user_login/login.html", context)


def logout_view(request):
    auth_facade_instance.logout(request)

    messages.info(request, "You have been logged out.")
    return redirect("home")