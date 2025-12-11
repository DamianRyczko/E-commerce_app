from .interfaces import IAuthFacade
from .repositories import DjangoAuthRepository
from .services import AuthService
from .facade import AuthFacade


def get_auth_facade() -> IAuthFacade:

    auth_repo = DjangoAuthRepository()

    auth_service = AuthService(repo=auth_repo)

    return AuthFacade(service=auth_service)


auth_facade_instance = get_auth_facade()