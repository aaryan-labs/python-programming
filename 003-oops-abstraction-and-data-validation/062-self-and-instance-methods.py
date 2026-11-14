"""
PYTHON ENGINEERING — MODULE 003
TOPIC 02: FUNCTIONS, INSTANCE METHODS, self AND METHOD BINDING

Run:
    python 062-self-and-instance-methods.py

Study sequence:
1. Read one section at a time.
2. Predict outputs before running prediction exercises.
3. Run the examples and inspect the results.
4. Complete the independent challenges.
5. Explain WHY, not just WHAT.

Scenario: Banking payment processing.
"""


# ============================================================
# SECTION 1: AN ORDINARY FUNCTION
# ============================================================

print("\n--- SECTION 1: ORDINARY FUNCTION ---")

def calculate_fee(amount):
    return amount * 0.02

print(calculate_fee(2000))

# An ordinary function receives information through its arguments.
# It has no automatic association with a Payment instance.


# ============================================================
# SECTION 2: A FUNCTION DEFINED INSIDE A CLASS
# ============================================================

print("\n--- SECTION 2: FUNCTION DEFINED IN A CLASS ---")

class Payment:
    def __init__(self, amount):
        self.amount = amount

    def calculate_fee(self):
        return self.amount * 0.02

payment_1 = Payment(1000)
payment_2 = Payment(5000)

print(payment_1.calculate_fee())
print(payment_2.calculate_fee())

# Called through an instance, the method can use that instance's state.
# The caller does not separately pass amount.


# ============================================================
# SECTION 3: AN EXTERNAL FUNCTION CAN ACCEPT AN OBJECT
# ============================================================

print("\n--- SECTION 3: EXTERNAL FUNCTION ACCEPTING AN OBJECT ---")

def calculate_payment_fee(payment):
    return payment.amount * 0.02

payment_1 = Payment(1000)
payment_2 = Payment(5000)

print(calculate_payment_fee(payment_1))
print(calculate_payment_fee(payment_2))

# It is entirely possible for an external function to accept an object.
# Choose between a function and a method based on responsibility:
# does the behavior naturally belong to the object, or is it independent?


# ============================================================
# SECTION 4: WHAT IS AN INSTANCE METHOD?
# ============================================================

print("\n--- SECTION 4: INSTANCE METHOD ---")

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def calculate_fee(self):
        return self.amount * 0.02

    def show_details(self):
        return f"{self.payment_id}: amount={self.amount}"

payment = Payment("TXN001", 1000)
print(payment.calculate_fee())
print(payment.show_details())

# An instance method is a function defined in a class that is normally
# called through an instance. Python supplies that instance as the
# first argument. By convention, that parameter is named self.


# ============================================================
# SECTION 5: THE SAME METHOD, DIFFERENT INSTANCE STATE
# ============================================================

print("\n--- SECTION 5: SAME METHOD, DIFFERENT INSTANCES ---")

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def apply_fee(self, fee):
        self.amount += fee

    def summary(self):
        return f"{self.payment_id}: {self.amount}"

payment_1 = Payment("TXN001", 1000)
payment_2 = Payment("TXN002", 2000)

payment_1.apply_fee(25)
payment_2.apply_fee(40)

print(payment_1.summary())
print(payment_2.summary())

# One method implementation serves both instances.
# Each call supplies a different instance as self.


# ============================================================
# SECTION 6: INSTANCE CALL AND EXPLICIT CLASS CALL
# ============================================================

print("\n--- SECTION 6: TWO WAYS TO CALL THE FUNCTION ---")

class Payment:
    def __init__(self, payment_id):
        self.payment_id = payment_id

    def show_id(self):
        print(self.payment_id)

payment = Payment("TXN001")
payment.show_id()
Payment.show_id(payment)

# Both calls execute the same function with payment as self.
# The instance-call form is preferred in normal application code.


# ============================================================
# SECTION 7: ACCESS THROUGH THE CLASS VERSUS THE INSTANCE
# ============================================================

print("\n--- SECTION 7: FUNCTION VERSUS BOUND METHOD ---")

class Payment:
    def calculate_fee(self):
        return 100

payment = Payment()

print(Payment.calculate_fee)
print(payment.calculate_fee)
print(type(Payment.calculate_fee))
print(type(payment.calculate_fee))

# Payment.calculate_fee accesses the underlying function.
# payment.calculate_fee accesses a bound method associated with payment.
# Accessing it does not execute it; parentheses execute the method.


# ============================================================
# SECTION 8: INSPECTING A BOUND METHOD
# ============================================================

print("\n--- SECTION 8: INSPECTING A BOUND METHOD ---")

class Payment:
    def __init__(self, payment_id):
        self.payment_id = payment_id

    def show_id(self):
        return self.payment_id

payment_1 = Payment("TXN001")
payment_2 = Payment("TXN002")
bound_method = payment_1.show_id

print(bound_method.__self__ is payment_1)
print(bound_method.__self__ is payment_2)
print(bound_method.__func__ is Payment.show_id)

# __self__ refers to the instance to which the method is bound.
# __func__ refers to the original function defined in the class.


# ============================================================
# SECTION 9: A BOUND METHOD STORED IN A VARIABLE
# ============================================================

print("\n--- SECTION 9: STORING A BOUND METHOD ---")

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def show_details(self):
        return f"{self.payment_id}: {self.amount}"

payment_1 = Payment("TXN001", 1000)
payment_2 = Payment("TXN002", 2000)

method = payment_1.show_details
payment_1.amount = 1500
payment_2.amount = 2500

print(method())
print(payment_1.show_details())
print(payment_2.show_details())

# method remains bound to payment_1 and reads its current state.


# ============================================================
# SECTION 10: self IS A REFERENCE TO THE INSTANCE
# ============================================================

print("\n--- SECTION 10: INSTANCE IDENTITY ---")

class Payment:
    def __init__(self, payment_id):
        self.payment_id = payment_id

    def show_identity(self):
        print("Inside method:", id(self))

payment = Payment("TXN001")
print("Outside method:", id(payment))
payment.show_identity()

# self refers to the same instance; it is not a copy.
# id() is unique for an object's lifetime, not a permanent identifier.


# ============================================================
# SECTION 11: self IS A CONVENTION, NOT A KEYWORD
# ============================================================

print("\n--- SECTION 11: self IS A CONVENTION ---")

class Demonstration:
    def show(instance_reference):
        print("Received object:", instance_reference)

demo = Demonstration()
demo.show()

# Python does not require the first parameter to be named self.
# self is nevertheless the universal convention; use it in normal code.


# ============================================================
# SECTION 12: THE INSTANCE PARAMETER
# ============================================================

print("\n--- SECTION 12: INSTANCE PARAMETER ---")

class Report:
    def display(self):
        print("Report ready")

report = Report()
report.display()

# If display were defined without a parameter, report.display() would
# still supply report, causing a TypeError because no parameter receives it.


# ============================================================
# SECTION 13: METHOD ARGUMENTS AND RETURN VALUES
# ============================================================

print("\n--- SECTION 13: METHOD ARGUMENTS AND RETURN VALUES ---")

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def is_high_value(self, threshold):
        return self.amount >= threshold

    def apply_fee(self, fee):
        self.amount += fee
        return self.amount

payment = Payment("TXN001", 25000)
result = payment.is_high_value(threshold=20000)
updated_amount = payment.apply_fee(50)

print(result)
print(updated_amount)

# self is supplied by the instance call. threshold and fee are ordinary
# arguments supplied by the caller. Returning a value aids reuse and testing.


# ============================================================
# SECTION 14: STATE-CHANGING VERSUS NON-MUTATING METHODS
# ============================================================

print("\n--- SECTION 14: METHOD RESPONSIBILITIES ---")

class Payment:
    def __init__(self, amount):
        self.amount = amount

    def fee_amount(self, rate):
        return self.amount * rate

    def add_fee(self, fee):
        self.amount += fee

payment = Payment(1000)
fee = payment.fee_amount(0.02)

print("Calculated fee:", fee)
print("Amount before adding fee:", payment.amount)

payment.add_fee(fee)
print("Amount after adding fee:", payment.amount)

# fee_amount calculates without changing state.
# add_fee changes the object's state. Method names should make this clear.


# ============================================================
# SECTION 15: PREDICTION EXERCISES
# ============================================================

"""
Predict every output before running. Explain WHY.

-----------------------------------------
EXERCISE 1 — FUNCTION AND INSTANCE METHOD
-----------------------------------------
def external_fee(amount):
    return amount * 0.02

class Payment:
    def __init__(self, amount):
        self.amount = amount
    def fee(self):
        return self.amount * 0.02

p1 = Payment(1000)
p2 = Payment(5000)
print(external_fee(2000))
print(p1.fee())
print(p2.fee())

---------------------------------------
EXERCISE 2 — EXPLICIT INSTANCE ARGUMENT
---------------------------------------
class Counter:
    def increase(self, amount):
        self.value += amount

counter = Counter()
counter.value = 10
counter.increase(5)
print(counter.value)
Counter.increase(counter, 7)
print(counter.value)

--------------------------------------
EXERCISE 3 — FUNCTION OR BOUND METHOD?
--------------------------------------
class Payment:
    def show(self):
        return "ready"

p = Payment()
print(type(Payment.show))
print(type(p.show))

--------------------------------------------
EXERCISE 4 — BOUND METHOD RETAINS INSTANCE I
--------------------------------------------
class Payment:
    def __init__(self, amount):
        self.amount = amount
    def show(self):
        return self.amount

p1 = Payment(1000)
p2 = Payment(2000)
method = p1.show
p1 = Payment(5000)

print(method())
print(p1.show())
print(p2.show())

---------------------------------------------
EXERCISE 5 — BOUND METHOD RETAINS INSTANCE II
---------------------------------------------
class Payment:
    def __init__(self, amount):
        self.amount = amount

    def show(self):
        return self.amount


p1 = Payment(1000)

method = p1.show

p1.amount = 2000

another_method = p1.show

p1 = Payment(3000)

print(method())
print(another_method())
print(p1.show())

-------------------------
EXERCISE 6 — METHOD STATE
-------------------------
class Wallet:
    def __init__(self, balance):
        self.balance = balance
    def add(self, amount):
        self.balance += amount
    def get_balance(self):
        return self.balance

w1 = Wallet(100)
w2 = Wallet(500)
w1.add(50)
print(w1.get_balance())
print(w2.get_balance())

--------------------------------
EXERCISE 7 — RETURN VERSUS PRINT
--------------------------------
class Payment:
    def __init__(self, amount):
        self.amount = amount
    def fee(self):
        print(self.amount * 0.02)

p = Payment(1000)
result = p.fee()
print(result)

Explain why the final print does not print the calculated fee.
Explanation:
    print(self.amount * 0.02) calculates 20.0 and displays it on the screen.
    However, displaying a value is not the same as returning it.
    Here is the crucial point:
        If a Python function does not explicitly return a value, Python implicitly returns None.
"""


# ============================================================
# SECTION 16: INDEPENDENT IMPLEMENTATION CHALLENGES
# ============================================================

"""
CHALLENGE 1 — PAYMENT FEE
Create Payment with payment_id and amount. Add calculate_fee(rate)
that returns the fee without changing amount.

CHALLENGE 2 — APPLY FEE
Add apply_fee(fee), changing only the calling instance's amount.
Demonstrate with two Payment objects.

CHALLENGE 3 — EXTERNAL FUNCTION
Write an external function accepting a Payment object and returning
its fee. Compare it with the instance-method implementation.

CHALLENGE 4 — BOUND METHOD
Store one instance's summary method in a variable. Change the instance's
amount and call the stored method. Explain which instance it uses.

CHALLENGE 5 — INSPECT BINDING
For a Payment instance p, inspect:
    Payment.calculate_fee
    p.calculate_fee
    p.calculate_fee.__self__
    p.calculate_fee.__func__

Explain what each expression refers to.

CHALLENGE 6 — METHOD DESIGN
Implement fee_amount(rate), which calculates without mutating, and
apply_fee(fee), which changes the payment amount. Test both.

Do not look up solutions immediately. Predict, implement, inspect,
and explain.
"""

print("\n--- FILE EXECUTED ---")
print("Complete the prediction exercises and independent challenges.")
