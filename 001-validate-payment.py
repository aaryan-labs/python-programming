# This is a sample Python script.
import math

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Main a collection of unique currencies
supported_currencies = {'INR', 'EUR', 'USD'}

def validate_payment(amount, currency, reference):

    is_amount_valid, is_currency_valid, is_reference_valid = False, False, False

    # Amount can not be negative
    # Not accepting strings/boolean
    if isinstance(amount, (int, float)) and not isinstance(amount, bool):
        if amount > 0 and math.isfinite(amount):
            is_amount_valid = True

    if currency in supported_currencies:
        is_currency_valid = True

    if isinstance(reference, str):
        if reference.strip() != "":
            is_reference_valid = True

    return {
            "is_amount_valid": is_amount_valid,
            "is_currency_valid": is_currency_valid,
            "is_reference_valid": is_reference_valid
        }

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    output = validate_payment(amount=100, currency='INR', reference='Family')
    print(output['is_amount_valid'], output['is_currency_valid'], output['is_reference_valid'])
    output = validate_payment(amount=100.50, currency='USD', reference='Salary')
    print(output['is_amount_valid'], output['is_currency_valid'], output['is_reference_valid'])
    output = validate_payment(amount=True, currency='INR', reference="Family")
    print(output['is_amount_valid'], output['is_currency_valid'], output['is_reference_valid'])
    output = validate_payment(amount=100, currency='INR', reference=None)
    print(output['is_amount_valid'], output['is_currency_valid'], output['is_reference_valid'])
    output = validate_payment(amount=100, currency='INR', reference=" ")
    print(output['is_amount_valid'], output['is_currency_valid'], output['is_reference_valid'])
    output = validate_payment(amount=-100, currency="INR", reference="Family")
    print(output['is_amount_valid'], output['is_currency_valid'], output['is_reference_valid'])
    output = validate_payment(amount=None, currency="INR", reference="Family")
    print(output['is_amount_valid'], output['is_currency_valid'], output['is_reference_valid'])
    output = validate_payment(amount=float('inf'), currency="INR", reference="Family")
    print(output['is_amount_valid'], output['is_currency_valid'], output['is_reference_valid'])