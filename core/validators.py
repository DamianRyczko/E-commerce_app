from django.core.exceptions import ValidationError
import datetime
import re


#---------------------------- ADDRESS ---------------------------
def validate_polish_zip(value):
    if not re.match(r'^\d{2}-\d{3}$', value):
        # You can use a standard f-string if you aren't translating
        raise ValidationError(
            f"{value} is not a valid zip code. Please use the 00-000 format."
        )

#---------------------------- PAYMENT  ---------------------------
def validate_blik_code(value):
    if not re.match(r'^\d{6}$', value):
        raise ValidationError(
            f"{value} is not a valid BLIK code. Please use 6 digits."
        )

def validate_card_number(value):
    if not re.match(r'^\d{16}$', value):
        raise ValidationError(
            f"{value} is not a valid card number. Please use 16 digits."
        )

def validate_card_date(value):
    #card date is stored as MM/YY string
    x = datetime.datetime.now()
    year = int(str(x.year)[2:])
    month = x.month
    value_month = int(value[:2])
    value_year = int(value[3:])
    print(year, month, value_year, value_month)
    if value_month < 0 or value_month > 12:
        raise ValidationError(f"{value} invalid date format")
    if value_year < year:
        raise ValidationError(
            f"{value} this card has expired"
        )
    if value_year == year:
        if value_month < month:
            raise ValidationError(
                f"{value} this card has expired"
            )

def validate_cvv(value):
    if not re.match(r'^\d{3}$', value):
        raise ValidationError(
            f"{value} is not a valid CVV code. Please use 3 digits."
        )

#---------------------------- PRODUCTS  ---------------------------
def validate_no_negative(value):
    value_int = float(value)
    if value_int < 0:
        raise ValidationError(
            f"{value} is not a valid price. Please use a positive number."
        )

