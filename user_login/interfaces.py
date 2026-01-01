from abc import ABC, abstractmethod
from typing import Any, Dict


class IAuthRepository(ABC):
    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> Any: pass

    @abstractmethod
    def create_customer(self, user: Any, customer_data: Dict[str, Any]) -> Any: pass

    @abstractmethod
    def add_user_to_group(self, user: Any, group_name: str) -> None: pass

    @abstractmethod
    def user_has_group(self, useer, user_group) -> bool: pass

class IAuthService(ABC):
    @abstractmethod
    def register_customer(self, user_data: Dict[str, Any], customer_data: Dict[str, Any]) -> Any: pass

    @abstractmethod
    def login_user(self, request: Any, user: Any) -> None: pass

    @abstractmethod
    def logout_user(self, request: Any) -> None: pass

    @abstractmethod
    def get_post_login_redirect_url(self, user) -> Any: pass


class IAuthFacade(ABC):
    @abstractmethod
    def register(self, user_form_data: Dict[str, Any], customer_form_data: Dict[str, Any]) -> Any: pass

    @abstractmethod
    def login(self, request: Any, user: Any) -> None: pass

    @abstractmethod
    def logout(self, request: Any) -> None: pass

    @abstractmethod
    def get_redirect_url(self, user) -> Any: pass