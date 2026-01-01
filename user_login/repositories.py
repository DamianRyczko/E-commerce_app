from django.contrib.auth.models import User, Group
from .interfaces import IAuthRepository
from core.models import Customer

class DjangoAuthRepository(IAuthRepository):
    def create_user(self, user_data):
        return User.objects.create_user(**user_data)

    def create_customer(self, user, customer_data):
        return Customer.objects.create(user=user, **customer_data)

    def add_user_to_group(self, user, group_name):
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

    def user_has_group(self, user, group_name):
        return user.groups.filter(name=group_name).exists()