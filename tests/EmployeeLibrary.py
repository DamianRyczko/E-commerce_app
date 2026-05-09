import os
import sys
from pathlib import Path
import django
from django.conf import settings
from django.core.management import call_command

# ===================== 0. FIX PATHS =====================
# Ensure Python can find the 'E-commarce_app' module
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
sys.path.append(str(project_root))

# ===================== 1. ENVIRONMENT CONFIGURATION =====================
# We don't set DJANGO_SETTINGS_MODULE env var here because we are manually configuring.

if not settings.configured:
    import SklepInternetowyZKotami.settings as project_settings

    # 1. Extract all uppercase settings from your project's settings.py
    #    This copies SECRET_KEY, INSTALLED_APPS, etc.
    custom_settings = {}
    for key in dir(project_settings):
        if key.isupper():
            custom_settings[key] = getattr(project_settings, key)

    # 2. Force the Database to be In-Memory (SQLite)
    custom_settings['DATABASES'] = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    # 3. Configure Django
    #    IMPORTANT: We do NOT pass 'default_settings=project_settings'.
    #    By passing our settings as **kwargs, Django uses global_settings
    #    as the fallback for missing keys (like LOGGING_CONFIG).
    settings.configure(**custom_settings)

django.setup()

# ===================== 2. IMPORTS =====================
# Must happen AFTER django.setup()
from core.factory import get_employee_facade
from core.models import Product, Category


class EmployeeLibrary:
    """
    Robot Framework Library for testing the Employee Facade.
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        print("--- Migrating In-Memory Database ---")
        call_command('migrate', verbosity=0)
        self.facade = get_employee_facade()

    def teardown_database(self):
        """Cleans data between tests"""
        Product.objects.all().delete()
        Category.objects.all().delete()

    # ===================== CATEGORY HELPERS =====================

    def create_category_via_facade(self, title, description="Test Description"):
        category = Category(title=title, description=description)
        self.facade.save_category(category)
        return category.id

    def update_category_via_facade(self, category_id, title, description="Updated Test Description"):
        category = Category.objects.get(id=category_id)
        category.title = title
        category.description = description
        self.facade.save_category(category)
        return category.id

    def delete_category_via_facade(self, category_id):
        self.facade.delete_category(category_id)

    def category_should_exist(self, title):
        if not Category.objects.filter(title=title).exists():
            raise AssertionError(f"Category '{title}' was expected in DB but not found.")

    def category_should_not_exist(self, title):
        if Category.objects.filter(title=title).exists():
            raise AssertionError(f"Category '{title}' should have been deleted but still exists.")

    def category_should_have_description(self, category_id, description):
        category = Category.objects.get(id=category_id)
        if description != category.description:
            raise AssertionError(f"Category '{category.title}' should have description: {description} but has {category.description}")

    # ===================== PRODUCT HELPERS =====================

    def create_product_via_facade(self, title, price, category_id, inventory=10):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValueError(f"Cannot create product: Category ID {category_id} not found.")

        product = Product(
            title=title,
            description=f"Description for {title}",
            price=price,
            inventory=inventory,
            category=category,
            image="placeholder.jpg"
        )
        try:
            product.full_clean()
        except Exception as e:
            # Re-raise as a standard error so Robot can catch it
            raise ValueError(f"Validation failed: {e}")

        self.facade.save_product(product)
        return product.id

    def update_product_via_facade(self, product_id, title, price, category_id):
        """
        Updates an existing product.
        Notice we pass 'product_id' so Django knows to UPDATE, not INSERT.
        """
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValueError(f"Category ID {category_id} not found.")

        # Option A: Fetch, modify, save (Safer)
        product = Product.objects.get(id=product_id)
        product.title = title
        product.price = price
        product.category = category

        # Option B: Re-instantiate with ID (Faster, works if you replace all fields)
        # product = Product(
        #     id=product_id,  # <--- CRITICAL: This triggers an UPDATE
        #     title=title,
        #     description=f"Updated Description for {title}",
        #     price=price,
        #     inventory=10,
        #     category=category,
        #     image="placeholder.jpg"
        # )

        self.facade.save_product(product)
        return product.id


    def delete_product_via_facade(self, product_id):
        self.facade.delete_product(product_id)

    def product_should_exist(self, title):
        if not Product.objects.filter(title=title).exists():
            raise AssertionError(f"Product '{title}' was expected in DB but not found.")

    def product_should_not_exist(self, title):
        if Product.objects.filter(title=title).exists():
            raise AssertionError(f"Product '{title}' should have been deleted but still exists.")

    def product_should_have_price(self, product_id, expected_price):
        product = Product.objects.get(id=product_id)
        if float(product.price) != float(expected_price):
            raise AssertionError(f"Expected price {expected_price}, but got {product.price}")