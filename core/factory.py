from .interfaces import ICustomerFacade, IEmployeeFacade
from .repositories import (
    DjangoCartRepository,
    DjangoOrderRepository,
    DjangoCustomerRepository,
    DjangoProductRepository,
    DjangoAddressRepository,
    DjangoCategoryRepository
)
from .services import (
    CartService,
    OrderService,
    CustomerService,
    ProductService,
    AddressService,
    CategoryService
)
from .facades import CustomerFacade, EmployeeFacade

cart_repo = DjangoCartRepository()
order_repo = DjangoOrderRepository()
customer_repo = DjangoCustomerRepository()
product_repo = DjangoProductRepository()
address_repo = DjangoAddressRepository()
category_repo = DjangoCategoryRepository()


cart_service = CartService(repo=cart_repo)
order_service = OrderService(repo=order_repo)
customer_service = CustomerService(repo=customer_repo)
product_service = ProductService(repo=product_repo)
address_service = AddressService(repo=address_repo)
category_service = CategoryService(repo=category_repo)


def get_customer_facade() -> ICustomerFacade:
    return CustomerFacade(
        cart_service=cart_service,
        order_service=order_service,
        customer_service=customer_service,
        product_service=product_service,
        address_service=address_service,
        category_service=category_service
    )

def get_employee_facade() -> IEmployeeFacade:
    return EmployeeFacade(
        cart_service=cart_service,
        order_service=order_service,
        customer_service=customer_service,
        product_service=product_service,
        address_service=address_service,
        category_service=category_service
    )

customer_facade: ICustomerFacade = get_customer_facade()
employee_facade: IEmployeeFacade = get_employee_facade()