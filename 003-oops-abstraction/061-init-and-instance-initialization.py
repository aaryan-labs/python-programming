"""
PYTHON ENGINEERING — MODULE 003
TOPIC: __init__, OBJECT INITIALISATION AND INSTANCE STATE

Run:
    python 061-init-and-instance-initialization.py

Study method:
1. Read the explanation and inspect the code.
2. Predict outputs before running the prediction exercises.
3. Run the file and compare.
4. Complete the independent challenges without looking up solutions.
5. Explain WHY, not just WHAT.

Scenario: Banking payment processing.
"""

# ============================================================
# SECTION 1: A CLASS AND ITS INSTANCES
# ============================================================

print("\n--- SECTION 1: CLASS AND INSTANCES ---")

class Payment:
    pass

payment_1 = Payment()
payment_2 = Payment()

print(type(payment_1))
print(payment_1 is payment_2)

# Payment is a class. Calling Payment() creates an instance.
# These two calls create two distinct objects.


# ============================================================
# SECTION 2: WHAT DOES __init__ DO?
# ============================================================

print("\n--- SECTION 2: INITIALISING AN INSTANCE ---")

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

payment_1 = Payment("TXN001", 1500)
payment_2 = Payment("TXN002", 2750)

print(payment_1.payment_id, payment_1.amount)
print(payment_2.payment_id, payment_2.amount)

# When Payment(...) is called, Python creates an instance and calls
# __init__ to initialize it.
# Technically, __new__ creates/returns the instance; __init__ initializes it.
# In normal application code, you generally define __init__, not __new__.

# ============================================================
# SECTION 3: EACH INSTANCE GETS ITS OWN STATE
# ============================================================

print("\n--- SECTION 3: INSTANCE-SPECIFIC STATE ---")

class Payment:
    def __init__(self, payment_id):
        self.payment_id = payment_id
        self.transactions = []

payment_1 = Payment("TXN001")
payment_2 = Payment("TXN002")

payment_1.transactions.append(1000)
payment_2.transactions.append(2000)

print(payment_1.transactions)
print(payment_2.transactions)
print(payment_1.transactions is payment_2.transactions)

# Each call to __init__ executes self.transactions = [].
# Each execution creates a NEW list, owned by that instance.


# ============================================================
# SECTION 4: CONTRAST — A CLASS ATTRIBUTE
# ============================================================

print("\n--- SECTION 4: CLASS ATTRIBUTE LOOKUP ---")

class Payment:
    currency = "INR"

    def __init__(self, payment_id):
        self.payment_id = payment_id

payment_1 = Payment("TXN001")
payment_2 = Payment("TXN002")

print(payment_1.currency)
print(payment_2.currency)
print(Payment.currency)

# currency is defined on the class, not in __init__.
# Attribute lookup checks the instance first, then the class.
# Both instances can access the one class attribute; neither gets a copy.


# ============================================================
# SECTION 5: INSTANCE ASSIGNMENT DOES NOT CHANGE THE CLASS
# ============================================================

print("\n--- SECTION 5: INSTANCE ATTRIBUTE SHADOWING ---")

class Payment:
    currency = "INR"

    def __init__(self, payment_id):
        self.payment_id = payment_id

payment_1 = Payment("TXN001")
payment_2 = Payment("TXN002")

payment_1.currency = "EUR"

print(payment_1.currency)
print(payment_2.currency)
print(Payment.currency)

# payment_1.currency = "EUR" creates an attribute on payment_1.
# It does NOT change Payment.currency.
# payment_2 still finds the class attribute.


# ============================================================
# SECTION 6: CHANGING THE CLASS ATTRIBUTE
# ============================================================

print("\n--- SECTION 6: CLASS ATTRIBUTE ASSIGNMENT ---")

class Payment:
    currency = "INR"

    def __init__(self, payment_id):
        self.payment_id = payment_id

payment_1 = Payment("TXN001")
payment_2 = Payment("TXN002")

Payment.currency = "USD"

print(payment_1.currency)
print(payment_2.currency)
print(Payment.currency)

# Assignment through Payment changes the class attribute itself.
# Instances without their own currency attribute now see "USD".


# ============================================================
# SECTION 7: THE MUTABLE CLASS ATTRIBUTE TRAP
# ============================================================

print("\n--- SECTION 7: SHARED MUTABLE CLASS ATTRIBUTE ---")

class Payment:
    transactions = []

    def __init__(self, payment_id):
        self.payment_id = payment_id

    def add_transaction(self, amount):
        self.transactions.append(amount)

payment_1 = Payment("TXN001")
payment_2 = Payment("TXN002")

payment_1.add_transaction(1000)
payment_2.add_transaction(2000)

print(payment_1.transactions)
print(payment_2.transactions)
print(Payment.transactions)

# Both instances find transactions on the class.
# Both retrieve the SAME list object. append() mutates that shared list.
# This is usually a bug when each payment should own its own transactions.
#
# Correct design:
#
# class Payment:
#     def __init__(self, payment_id):
#         self.payment_id = payment_id
#         self.transactions = []


# ============================================================
# SECTION 8: ASSIGNMENT VS MUTATION
# ============================================================

print("\n--- SECTION 8: ASSIGNMENT VS MUTATION ---")

class Payment:
    transactions = []

    def __init__(self, payment_id):
        self.payment_id = payment_id

payment_1 = Payment("TXN001")
payment_2 = Payment("TXN002")

payment_1.transactions = [1000]  # Assignment: creates instance attribute.

print("After assignment:")
print(payment_1.transactions)
print(payment_2.transactions)
print(Payment.transactions)

# Fresh class and instances for the mutation example.
class Payment:
    transactions = []

    def __init__(self, payment_id):
        self.payment_id = payment_id

payment_1 = Payment("TXN001")
payment_2 = Payment("TXN002")

payment_1.transactions.append(1000)  # Mutation: changes shared list.

print("After mutation:")
print(payment_1.transactions)
print(payment_2.transactions)
print(Payment.transactions)

# Assignment binds an attribute on payment_1.
# Mutation changes the list object returned by attribute lookup.


# ============================================================
# SECTION 9: PREDICTION EXERCISES
# ============================================================

"""
Predict every output BEFORE running each exercise. Explain WHY.
-----------------------------------------
EXERCISE 1 — Separate instance attributes
-----------------------------------------
class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

a1 = Account("A001", 5000)
a2 = Account("A002", 8000)
a1.balance += 500

print(a1.balance)
print(a2.balance)

----------------------------------------------
EXERCISE 2 — Class attribute lookup and update
----------------------------------------------
class Account:
    account_type = "SAVINGS"

    def __init__(self, account_id):
        self.account_id = account_id

a1 = Account("A001")
a2 = Account("A002")

print(a1.account_type)
print(a2.account_type)

Account.account_type = "CURRENT"

print(a1.account_type)
print(a2.account_type)

-------------------------------
EXERCISE 3 — Instance shadowing
-------------------------------
class Account:
    account_type = "SAVINGS"

    def __init__(self, account_id):
        self.account_id = account_id

a1 = Account("A001")
a2 = Account("A002")
a1.account_type = "CURRENT"

print(a1.account_type)
print(a2.account_type)
print(Account.account_type)

-------------------------------------------
EXERCISE 4 — Shared mutable class attribute
-------------------------------------------
class Account:
    notes = []

    def __init__(self, account_id):
        self.account_id = account_id

a1 = Account("A001")
a2 = Account("A002")
a1.notes.append("Review required")

print(a1.notes)
print(a2.notes)
print(Account.notes)

----------------------------------------------------
EXERCISE 5 — Independent mutable instance attributes
----------------------------------------------------
class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self.notes = []

a1 = Account("A001")
a2 = Account("A002")
a1.notes.append("Review required")

print(a1.notes)
print(a2.notes)
"""


# ============================================================
# SECTION 10: INDEPENDENT IMPLEMENTATION
# ============================================================

"""
CHALLENGE 1 — PAYMENT INITIALISATION
Implement Payment with payment_id, amount, currency (default "INR"),
and transactions (initially an empty list). Create two payments and
demonstrate independent transaction lists.

CHALLENGE 2 — CLASS ATTRIBUTE
Add a class attribute payment_network = "UPI". Access it through two
instances and through the class.

CHALLENGE 3 — SHADOWING
Assign a different payment_network to only the first instance.
Print it through both instances and through the class. Explain.

CHALLENGE 4 — DEBUG THE DESIGN
A developer defines transactions = [] in the class body. Two payment
instances unexpectedly show each other's transactions. Explain why
and correct the implementation.

CHALLENGE 5 — EXPLAIN THE LIFECYCLE
Explain what happens when this executes:
    payment = Payment("TXN001", 1500)

Include instance creation, __init__, self, and instance attributes.

Do not look up solutions immediately. Predict, implement, inspect,
and explain.
"""

print("\n--- FILE EXECUTED ---")
print("Complete the prediction and independent implementation exercises.")
