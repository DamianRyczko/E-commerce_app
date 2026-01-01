from django.contrib.auth import login as django_login, logout as django_logout
from django.db import transaction
from .interfaces import IAuthRepository, IAuthService
class AuthService(IAuthService):
    def __init__(self, repo: IAuthRepository):
        self.repo = repo

    def register_customer(self, user_data, customer_data):
        with transaction.atomic():
            user = self.repo.create_user(user_data)
            self.repo.create_customer(user, customer_data)
            self.repo.add_user_to_group(user, 'Customers')
            return user

    def get_post_login_redirect_url(self, user):
        if self.repo.user_has_group(user, 'Admins'):
            return "admin:index"
        elif self.repo.user_has_group(user, 'Employees'):
            return "employee_products"
        else:
            return "home"

    def login_user(self, request, user):
        # Adapter do mechanizmu sesji Django
        django_login(request, user)

    def logout_user(self, request):
        django_logout(request)