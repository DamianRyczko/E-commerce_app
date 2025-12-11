from django.contrib.auth.models import User
from .interfaces import IAuthRepository
from core.models import Customer

class DjangoAuthRepository(IAuthRepository):
    def create_user(self, user_data):
        return User.objects.create_user(**user_data)

    def create_customer(self, user, customer_data):
        return Customer.objects.create(user=user, **customer_data)