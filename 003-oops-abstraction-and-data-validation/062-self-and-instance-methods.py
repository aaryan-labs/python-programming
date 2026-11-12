"""
PYTHON ENGINEERING — MODULE 03
TOPIC 02: self — INSTANCE REFERENCES AND METHOD BINDING

Run: python 02_self_and_instance_methods.py

Read the explanations, predict outputs, run the file, then complete
the independent challenges. Explain WHY, not just WHAT.

Scenario: Banking payment processing.
"""

# ============================================================
# SECTION 1: WHAT DOES self REFER TO?
# ============================================================
print("\n--- SECTION 1: self REFERS TO THE CURRENT INSTANCE ---")

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def show_details(self):
        print(self.payment_id, self.amount)

payment_1 = Payment("TXN001", 1500)
payment_2 = Payment("TXN002", 2750)
payment_1.show_details()
payment_2.show_details()

# self refers to the particular instance on which the method is called.
# During payment_1.show_details(), self refers to payment_1.
# During payment_2.show_details(), self refers to payment_2.
# self is a conventional parameter name, not a Python keyword.


# ============================================================
# SECTION 2: PYTHON PASSES THE INSTANCE AUTOMATICALLY
# ============================================================
print("\n--- SECTION 2: AUTOMATIC INSTANCE PASSING ---")

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def apply_fee(self, fee):
        self.amount += fee

payment_1 = Payment("TXN001", 1500)
payment_2 = Payment("TXN002", 2750)
payment_1.apply_fee(50)
payment_2.apply_fee(100)
print(payment_1.amount)
print(payment_2.amount)

# payment_1.apply_fee(50) is effectively:
# Payment.apply_fee(payment_1, 50)
# Python supplies the instance as the first argument; it is received
# by self. The value 50 is received by fee.


# ============================================================
# SECTION 3: ONE METHOD, DIFFERENT INSTANCE STATE
# ============================================================
print("\n--- SECTION 3: ONE METHOD, DIFFERENT OBJECTS ---")

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def apply_discount(self, discount):
        self.amount -= discount

    def summary(self):
        return f"{self.payment_id}: {self.amount}"

payments = [
    Payment("TXN001", 1000),
    Payment("TXN002", 2000),
    Payment("TXN003", 3000),
]

for payment in payments:
    payment.apply_discount(100)
    print(payment.summary())

# The class defines one method implementation. Each call supplies a
# different instance as self, so the method operates on that instance.

# ============================================================
# SECTION 4: EXPLICIT METHOD CALL
# ============================================================
print("\n--- SECTION 4: EXPLICIT INSTANCE PASSING ---")

class Payment:
    def show_id(self):
        print(self.payment_id)

payment_1 = Payment()
payment_1.payment_id = "TXN001"

payment_1.show_id()          # Normal instance call
Payment.show_id(payment_1)  # Explicitly supply the instance

# Both calls supply payment_1 as self. The normal instance call is
# preferred in ordinary application code.


# ============================================================
# SECTION 5: self IS A REFERENCE, NOT A COPY
# ============================================================
print("\n--- SECTION 5: OBJECT IDENTITY ---")

class Payment:
    def __init__(self, payment_id):
        self.payment_id = payment_id

    def show_identity(self):
        print("Inside method:", id(self))

payment_1 = Payment("TXN001")
print("Outside method:", id(payment_1))
payment_1.show_identity()

# The IDs match: self refers to the same instance as payment_1.
# self is not a new Payment object and is not a copy of the instance.


# ============================================================
# SECTION 6: self IS A CONVENTION, NOT A KEYWORD
# ============================================================
print("\n--- SECTION 6: CONVENTIONAL PARAMETER NAME ---")

class Demonstration:
    def show(instance_reference):
        print("Received object:", instance_reference)

demo = Demonstration()
demo.show()

# Python does not require the first parameter to be named self.
# However, self is the standard convention and should be used in
# normal Python code. This example is for understanding only.


# ============================================================
# SECTION 7: FORGETTING THE INSTANCE PARAMETER
# ============================================================
print("\n--- SECTION 7: CORRECT INSTANCE METHOD SIGNATURE ---")

class Payment:
    def __init__(self, payment_id):
        self.payment_id = payment_id

    # An instance method defined as def show_id(): has no parameter
    # to receive the instance Python supplies during payment.show_id().
    def show_id(self):
        print("Payment ID:", self.payment_id)

payment = Payment("TXN001")
payment.show_id()


# ============================================================
# SECTION 8: READ INSTANCE STATE AND RETURN A RESULT
# ============================================================
print("\n--- SECTION 8: INSTANCE METHOD RETURN VALUE ---")

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def is_high_value(self, threshold):
        return self.amount >= threshold

payment = Payment("TXN001", 25000)
result = payment.is_high_value(20000)
print("High-value payment?", result)

# self lets the method read this instance's amount.
# threshold is a separate argument supplied by the caller.
# Returning a value makes the method reusable and straightforward to test.


# ============================================================
# SECTION 9: PREDICTION EXERCISES
# ============================================================
"""
Predict every output BEFORE running each exercise. Explain WHY.

EXERCISE 1 — Which instance is self?
class Customer:
    def __init__(self, name):
        self.name = name
    def greet(self):
        print("Hello", self.name)
c1 = Customer("Ayesha")
c2 = Customer("Ravi")
c1.greet()
c2.greet()

EXERCISE 2 — Method call equivalence
class Counter:
    def increase(self, amount):
        self.value += amount
counter = Counter()
counter.value = 10
counter.increase(5)
print(counter.value)
Counter.increase(counter, 7)
print(counter.value)

EXERCISE 3 — Separate object state
class Wallet:
    def __init__(self, balance):
        self.balance = balance
    def add_money(self, amount):
        self.balance += amount
w1 = Wallet(100)
w2 = Wallet(500)
w1.add_money(50)
print(w1.balance)
print(w2.balance)

EXERCISE 4 — self is not a copy
class Probe:
    def inspect(self):
        print(id(self))
p = Probe()
print(id(p))
p.inspect()

EXERCISE 5 — Missing instance parameter
class Report:
    def display():
        print("Report ready")
r = Report()
r.display()

Predict whether this runs successfully. If not, explain why and
write the corrected method signature.
"""


# ============================================================
# SECTION 10: INDEPENDENT IMPLEMENTATION
# ============================================================
"""
CHALLENGE 1 — PAYMENT SUMMARY
Create Payment with payment_id and amount. Add summary() that returns
both values in a readable string. Create two instances and call it.

CHALLENGE 2 — APPLY FEE
Add apply_fee(fee). It must increase only the amount belonging to the
instance on which the method is called. Demonstrate with two payments.

CHALLENGE 3 — VALIDATE AMOUNT
Add is_valid() returning True when this instance's amount is positive,
otherwise False. Test at least two instances.

CHALLENGE 4 — EXPLAIN THE CALL
For payment.apply_fee(25), explain which object receives the call,
what self refers to, what fee receives, and whose amount changes.

CHALLENGE 5 — EXPLICIT CALL
Call both:
    payment.apply_fee(25)
    Payment.apply_fee(payment, 25)
Verify that both forms operate on the same instance.

Do not look up solutions immediately. Predict, implement, inspect,
and explain.
"""

print("\n--- FILE EXECUTED ---")
print("Complete the prediction and independent implementation exercises.")
