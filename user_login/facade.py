from .interfaces import IAuthFacade, IAuthService

class AuthFacade(IAuthFacade):
    def __init__(self, service: IAuthService):
        self.service = service

    def register(self, user_form_data, customer_form_data):
        return self.service.register_customer(user_form_data, customer_form_data)

    def login(self, request, user):
        self.service.login_user(request, user)

    def logout(self, request):
        self.service.logout_user(request)