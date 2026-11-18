"""
AI Engineering Academy — Python Engineering
Module 004 | Topic 004.01 — Pydantic, Data Validation and Serialization
Roadmap: Module 004 Roadmap V2.0

Install: python -m pip install "pydantic>=2,<3"
Run:     python 081-pydantic-validation.py

This is a guided practice file. Read and run it from top to bottom.
Pydantic checks whether data follows rules you define. It does not prove
that the data is factually true.
"""

from typing import Literal
import unittest

from pydantic import BaseModel, Field, ValidationError


# 1. WHY CHECK DATA?
# ------------------
# A dictionary accepts values without enforcing our application's rules.
raw_customer = {
    "customer_id": "1001",  # String, not an integer
    "name": "Ravi",
    "age": "thirty",        # Not a number
}
print("\n1. Ordinary dictionary:", raw_customer)


# 2. FIRST MODEL
# --------------
class Customer(BaseModel):
    customer_id: int
    name: str
    email: str


# Pydantic converts compatible input, such as "1001", into integer 1001.
customer = Customer(
    customer_id="1001",
    name="Ravi Kumar",
    email="ravi@example.com",
)
print("\n2. Validated customer:", customer)
print("customer_id type:", type(customer.customer_id).__name__)

# An ordinary Python type label is guidance, not automatic enforcement:
#     customer_id: int = "ABC123"
# Python permits that assignment. Pydantic uses model field types as rules
# when creating or validating a model.


# 3. INVALID INPUT
# ----------------
print("\n3. Invalid input:")
try:
    Customer(
        customer_id="not-a-number",
        name="Ravi",
        email="ravi@example.com",
    )
except ValidationError as error:
    print("Pydantic rejected the input:")
    print(error)


# 4. FIELD RESTRICTIONS AND DEFAULTS
# ---------------------------------
class CustomerRecord(BaseModel):
    customer_id: int = Field(gt=0)             # Greater than zero
    name: str = Field(min_length=1, max_length=60)
    email: str = Field(min_length=3, max_length=120)
    city: str = Field(default="Bengaluru")


valid_customer = CustomerRecord(
    customer_id="101",
    name="Anita",
    email="anita@example.com",
)
print("\n4. Customer with default city:", valid_customer)

mumbai_customer = CustomerRecord(
    customer_id=102,
    name="Meera",
    email="meera@example.com",
    city="Mumbai",
)
print("Supplied city overrides default:", mumbai_customer.city)

# gt=0 means greater than zero; ge=0 means greater than or equal to zero.
# Try customer_id=0 and name="" to see the restrictions reject the values.


# 5. OPTIONAL FIELDS AND RESTRICTED CHOICES
# ----------------------------------------
class Order(BaseModel):
    order_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    total_amount: float = Field(ge=0)
    status: Literal["Pending", "Paid", "Failed", "Refunded"]
    notes: str | None = None


# str | None allows text or None. The default None means notes may be omitted.
# Literal restricts status to the exact listed choices.
order = Order(
    order_id=501,
    customer_id=101,
    total_amount="2500",
    status="Paid",
)
print("\n5. Valid order:", order)

try:
    Order(
        order_id=502,
        customer_id=101,
        total_amount=100,
        status="Processing",  # Not an allowed choice
    )
except ValidationError as error:
    print("Invalid status rejected:")
    print(error)


# 6. DICTIONARY TO MODEL
# ----------------------
raw_order = {
    "order_id": "503",
    "customer_id": "101",
    "total_amount": "1250.50",
    "status": "Pending",
}
order_from_dict = Order.model_validate(raw_order)
print("\n6. Dictionary validated:", order_from_dict)
# model_validate() is built into Pydantic's BaseModel. It accepts a dictionary.


# 7. JSON TEXT TO MODEL
# ---------------------
order_json = """{
    "order_id": 504,
    "customer_id": 101,
    "total_amount": 800.0,
    "status": "Paid",
    "notes": "Payment confirmed"
}"""
order_from_json = Order.model_validate_json(order_json)
print("\n7. JSON validated:", order_from_json)
# model_validate_json() accepts JSON text.


# 8. MODEL TO DICTIONARY OR JSON TEXT
# ----------------------------------
payment_order = Order(
    order_id=505,
    customer_id=101,
    total_amount=2500,
    status="Paid",
)
print("\n8. Python dictionary:", payment_order.model_dump())
print("JSON text:", payment_order.model_dump_json())
# model_dump() returns a Python dictionary.
# model_dump_json() returns JSON text.


# 9. NESTED MODELS
# ----------------
class Address(BaseModel):
    city: str
    state: str
    pin_code: str = Field(min_length=6, max_length=6)


class Employee(BaseModel):
    employee_id: int = Field(gt=0)
    name: str = Field(min_length=1)
    address: Address
    skills: list[str]


employee_data = {
    "employee_id": 7001,
    "name": "Asha",
    "address": {
        "city": "Bengaluru",
        "state": "Karnataka",
        "pin_code": "560001",
    },
    "skills": ["Python", "SQL"],
}
employee = Employee.model_validate(employee_data)
print("\n9. Nested employee:", employee)
print("Employee city:", employee.address.city)


# 10. AI-GENERATED STRUCTURED OUTPUT
# ----------------------------------
class SupportTicketResult(BaseModel):
    category: Literal["Payments", "Fraud", "Account", "Technical"]
    confidence: Literal["Low", "Medium", "High"]
    reason: str = Field(min_length=10, max_length=300)


ai_response = """{
    "category": "Fraud",
    "confidence": "High",
    "reason": "The transaction pattern differs from usual activity."
}"""
ticket = SupportTicketResult.model_validate_json(ai_response)
print("\n10. Checked AI output:", ticket)
# This checks format and permitted values, not whether the AI conclusion is true.


# 11. BANKING PAYMENT EXAMPLE
# ---------------------------
class Payment(BaseModel):
    payment_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    currency: Literal["INR", "USD", "EUR"]
    status: Literal["Pending", "Completed", "Failed"]
    remarks: str | None = None


def accept_payment_data(data: dict) -> Payment:
    """Check incoming dictionary data before application logic uses it."""
    return Payment.model_validate(data)


incoming_payment = {
    "payment_id": "1001",
    "amount": "2500",
    "currency": "INR",
    "status": "Completed",
}
accepted_payment = accept_payment_data(incoming_payment)
print("\n11. Accepted payment:", accepted_payment)
print("Payment ID type:", type(accepted_payment.payment_id).__name__)


# 12. FOCUSED TESTS
# -----------------
class TestPaymentValidation(unittest.TestCase):
    def test_compatible_values_are_converted(self):
        item = Payment.model_validate({
            "payment_id": "1001",
            "amount": "2500",
            "currency": "INR",
            "status": "Completed",
        })
        self.assertEqual(item.payment_id, 1001)
        self.assertIsInstance(item.payment_id, int)
        self.assertEqual(item.amount, 2500.0)

    def test_zero_payment_id_is_rejected(self):
        with self.assertRaises(ValidationError):
            Payment(payment_id=0, amount=100, currency="INR", status="Pending")

    def test_zero_amount_is_rejected(self):
        with self.assertRaises(ValidationError):
            Payment(payment_id=1, amount=0, currency="INR", status="Pending")

    def test_unknown_currency_is_rejected(self):
        with self.assertRaises(ValidationError):
            Payment(payment_id=1, amount=100, currency="GBP", status="Pending")

    def test_optional_remarks_default_to_none(self):
        item = Payment(payment_id=1, amount=100, currency="INR", status="Pending")
        self.assertIsNone(item.remarks)

    def test_json_round_trip(self):
        original = Payment(
            payment_id=10, amount=500, currency="INR", status="Completed"
        )
        restored = Payment.model_validate_json(original.model_dump_json())
        self.assertEqual(restored, original)


# 13. INDEPENDENT PRACTICE — TRY BEFORE LOOKING UP HELP
# -----------------------------------------------------
# TASK A: Create Product with product_id (positive integer), name (non-empty
# text), price (greater than zero), and stock (zero or greater). Test valid and
# invalid products.
# TASK B: Restrict order status to Created, Processing, Completed, Cancelled.
# TASK C: Validate a dictionary where product_id and price are strings. Print
# their types after validation.
# TASK D: Convert a valid model to JSON text, then create a new model from it.
# TASK E: Explain why we validate before use, why validation does not prove
# truth, and when to use model_validate vs model_validate_json.
# HINTS: Field(gt=0), Field(ge=0), Literal[...], model_validate(),
# model_validate_json().


if __name__ == "__main__":
    print("\nRunning payment validation tests...")
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestPaymentValidation)
    )
    print("\nAll tests passed." if result.wasSuccessful() else "\nSome tests failed.")
