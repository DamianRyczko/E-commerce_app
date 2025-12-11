from abc import ABC, abstractmethod
from typing import Any, Dict


class IAuthRepository(ABC):
    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> Any: pass

    @abstractmethod
    def create_customer(self, user: Any, customer_data: Dict[str, Any]) -> Any: pass


class IAuthService(ABC):
    @abstractmethod
    def register_customer(self, user_data: Dict[str, Any], customer_data: Dict[str, Any]) -> Any: pass

    @abstractmethod
    def login_user(self, request: Any, user: Any) -> None: pass

    @abstractmethod
    def logout_user(self, request: Any) -> None: pass


class IAuthFacade(ABC):
    @abstractmethod
    def register(self, user_form_data: Dict[str, Any], customer_form_data: Dict[str, Any]) -> Any: pass

    @abstractmethod
    def login(self, request: Any, user: Any) -> None: pass

    @abstractmethod
    def logout(self, request: Any) -> None: pass