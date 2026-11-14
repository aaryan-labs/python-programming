"""
PYTHON ENGINEERING — MODULE 003
TOPIC 04: PROPERTIES AND ATTRIBUTE CONTROL

Run:
    python 064-properties-and-attribute-control.py

Study sequence:
1. Read one section at a time.
2. Understand the explanation comments before running the code.
3. Predict outputs where a prediction is requested.
4. Run the examples and inspect the results.
5. Complete the debugging exercises and independent challenges.
6. Explain WHY, not just WHAT.

Scenario: Banking and payment systems.

Prerequisites:
    - Classes, instances and instance attributes.
    - __init__ and self.
    - Instance methods and return values.
    - Object representation (__str__ and __repr__).

Scope:
    This file follows the properties topic introduced in VS Notebook 06.
    It develops the topic beyond the introductory example into validation,
    controlled attribute access, design trade-offs and testing.

Important:
    A property is an interface to an attribute-like operation.
    It does not automatically make an object immutable or secure.
"""


# ============================================================
# SECTION 1: WHY DO WE NEED PROPERTIES?
# ============================================================

print("\n--- SECTION 1: WHY DO WE NEED PROPERTIES? ---")

# A class can expose its data through ordinary instance attributes.
# This is simple and often perfectly appropriate.
#
# However, direct assignment gives callers the ability to place values
# into an attribute without the class checking whether those values
# satisfy the business rules.
#
# In a banking system, an account balance should not be changed
# arbitrarily by every caller. A payment amount may need to be positive.
#
# First, observe a class that exposes its data directly.

class BasicPayment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount


payment = BasicPayment("TXN001", 1500)

print("Initial amount:", payment.amount)

# The caller can assign another value directly.
# No validation is performed by this class.
payment.amount = -500

print("Amount after direct assignment:", payment.amount)

# The class has no control over the value assigned to amount.
# A property can provide a controlled interface while preserving
# attribute-like syntax for callers.


# ============================================================
# SECTION 2: METHODS, ATTRIBUTES AND PROPERTIES
# ============================================================

print("\n--- SECTION 2: METHODS, ATTRIBUTES AND PROPERTIES ---")

# An attribute stores or exposes information on an object.
# A method represents an operation that is called using parentheses.
#
# A property is implemented using methods, but callers access it
# using attribute syntax. This can be useful when retrieving a value
# is conceptually an attribute access rather than an explicit command.

class AccountSummary:
    def __init__(self, monthly_income):
        self.monthly_income = monthly_income

    def calculate_annual_income(self):
        # This is an ordinary method.
        # The caller must use parentheses to execute it.
        return self.monthly_income * 12

    @property
    def annual_income(self):
        # This method is exposed as a property.
        # The caller accesses it without parentheses.
        return self.monthly_income * 12


summary = AccountSummary(80000)

print("Monthly income attribute:", summary.monthly_income)
print("Annual income method:", summary.calculate_annual_income())
print("Annual income property:", summary.annual_income)

# Notice the syntax:
#     summary.calculate_annual_income()  -> method call
#     summary.annual_income              -> property access
#
# Do not choose a property merely to avoid parentheses.
# Choose it when the value behaves conceptually like an attribute.


# ============================================================
# SECTION 3: THE @property DECORATOR
# ============================================================

print("\n--- SECTION 3: THE @property DECORATOR ---")

# @property is a built-in decorator.
# It converts the method immediately below it into a property descriptor.
#
# The method name becomes the public attribute-like interface.
# The method body calculates or retrieves the value when accessed.
#
# The caller does not need to know that a method implements the property.

class Employee:
    def __init__(self, name, monthly_salary):
        self.name = name
        self.monthly_salary = monthly_salary

    @property
    def annual_salary(self):
        # Calculate the annual salary from the source value.
        # Do not store a second value that can become inconsistent.
        return self.monthly_salary * 12


employee = Employee("Ananya", 82000)

print("Employee:", employee.name)
print("Annual salary:", employee.annual_salary)

# Property access invokes the getter.
# This is not an ordinary stored instance attribute named annual_salary.
#
# The following would be incorrect:
#     employee.annual_salary()
#
# annual_salary is accessed like an attribute, not called like a method.


# ============================================================
# SECTION 4: COMPUTED PROPERTIES AND DERIVED STATE
# ============================================================

print("\n--- SECTION 4: COMPUTED PROPERTIES ---")

# A computed property derives a value from other attributes.
#
# If the derived value is stored independently, it can become stale.
# For example, if monthly_salary changes but annual_salary is not
# recalculated, the object can contain contradictory information.
#
# A computed property avoids storing redundant derived state.

class SalaryRecord:
    def __init__(self, employee_id, monthly_salary):
        self.employee_id = employee_id
        self.monthly_salary = monthly_salary

    @property
    def annual_salary(self):
        return self.monthly_salary * 12

    @property
    def monthly_salary_with_bonus_estimate(self):
        # This is only an illustrative calculation.
        # A real bonus policy would need explicit business rules.
        return self.monthly_salary * 1.10


record = SalaryRecord("EMP101", 75000)

print("Initial annual salary:", record.annual_salary)
print("Initial bonus estimate:", record.monthly_salary_with_bonus_estimate)

# Change the source attribute.
record.monthly_salary = 90000

# The computed properties now use the updated source value.
print("Updated annual salary:", record.annual_salary)
print("Updated bonus estimate:", record.monthly_salary_with_bonus_estimate)

# Engineering decision:
# Store source facts. Calculate derived facts when appropriate.
# Do not automatically create a property for every calculation.
# Consider calculation cost, consistency requirements and domain meaning.


# ============================================================
# SECTION 5: HOW A PROPERTY RESPONDS TO UNDERLYING CHANGES
# ============================================================

print("\n--- SECTION 5: PROPERTY AND UNDERLYING STATE ---")

# A property getter runs when the property is accessed.
# Unless the result is explicitly cached, the getter executes again
# on each access.
#
# The property below reads the current underlying attributes.

class Loan:
    def __init__(self, principal, annual_rate):
        self.principal = principal
        self.annual_rate = annual_rate

    @property
    def annual_interest(self):
        return self.principal * self.annual_rate

loan = Loan(500000, 0.09)

print("Annual interest:", loan.annual_interest)

loan.principal = 600000
print("Annual interest after principal changes:", loan.annual_interest)

loan.annual_rate = 0.10
print("Annual interest after rate changes:", loan.annual_interest)

# The property did not need to be manually updated.
# It recalculated using the current state each time it was accessed.
#
# A property is not automatically cached.
# If a calculation is expensive, evaluate whether a method, explicit
# caching strategy or another design is more appropriate.


# ============================================================
# SECTION 6: GETTERS AND SETTERS
# ============================================================

print("\n--- SECTION 6: GETTERS AND SETTERS ---")

# A getter controls how a value is read.
# A setter controls what happens when a caller assigns a value.
#
# The getter is created with @property.
# The setter is created with @<property_name>.setter.
#
# The public interface remains attribute-like:
#     payment.amount
#     payment.amount = 2500

class ValidatedPayment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        # Assignment invokes the amount setter.
        self.amount = amount

    @property
    def amount(self):
        # Return the internally stored value.
        return self._amount

    @amount.setter
    def amount(self, value):
        # Validate before changing the stored state.
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("Payment amount must be a number.")

        if value <= 0:
            raise ValueError("Payment amount must be positive.")

        self._amount = value


payment = ValidatedPayment("TXN002", 2500)

print("Initial payment amount:", payment.amount)

# This assignment invokes the setter.
payment.amount = 3000
print("Updated payment amount:", payment.amount)

# Try these assignments individually by uncommenting one at a time:
#
# payment.amount = -100
# payment.amount = "three thousand"
# payment.amount = True
#
# The setter rejects invalid values before updating _amount.


# ============================================================
# SECTION 7: PROPERTY VALIDATION AND OBJECT INVARIANTS
# ============================================================

print("\n--- SECTION 7: PROPERTY VALIDATION ---")

# An invariant is a condition that should remain true for an object
# throughout its valid lifetime.
#
# For a payment:
#     - amount must be numeric
#     - amount must be greater than zero
#
# Validation should happen at every public point where invalid state
# could otherwise enter the object.
#
# The setter is useful because both initialization and later assignment
# can use the same validation logic.

class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        # This invokes the setter defined below.
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Amount must be an integer or float.")

        if value <= 0:
            raise ValueError("Amount must be greater than zero.")

        self._amount = float(value)


valid_payment = Payment("TXN003", 1250)
print("Validated amount:", valid_payment.amount)

# The constructor also uses the setter.
# Therefore invalid initial values are rejected as well.
#
# Run these separately to observe the exceptions:
#
# Payment("TXN004", -50)
# Payment("TXN005", "1250")
#
# Important:
# A property setter protects assignment through the property.
# It does not make the internal _amount attribute inaccessible.
# Python's leading underscore is a convention, not a security boundary.


# ============================================================
# SECTION 8: READ-ONLY PROPERTIES
# ============================================================

print("\n--- SECTION 8: READ-ONLY PROPERTIES ---")

# A property with no setter is read-only through its public property name.
# Callers can read the value but cannot assign to that property.
#
# This is useful for derived information or values that should not be
# directly changed after construction.

class BankAccount:
    def __init__(self, account_number, opening_balance):
        self.account_number = account_number
        self._opening_balance = opening_balance

    @property
    def opening_balance(self):
        return self._opening_balance

    @property
    def account_label(self):
        # A derived, read-only value.
        return f"Account ending {self.account_number[-4:]}"


account = BankAccount("123456789012", 10000)

print("Opening balance:", account.opening_balance)
print("Account label:", account.account_label)

# The following assignments raise AttributeError because no setter exists:
#
# account.opening_balance = 5000
# account.account_label = "New label"
#
# Read-only through the property does not mean the entire object is immutable.
# Other attributes may still be mutable, and underscore attributes remain
# accessible by convention.


# ============================================================
# SECTION 9: PROPERTY DELETERS
# ============================================================

print("\n--- SECTION 9: PROPERTY DELETERS ---")

# A property can define a deleter using @<property_name>.deleter.
# The deleter runs when the caller executes del object.property_name.
#
# Deleters are less common than getters and setters.
# Use them only when deletion has a clear and meaningful domain behaviour.
#
# This example represents an optional contact detail.

class Customer:
    def __init__(self, customer_id, email):
        self.customer_id = customer_id
        self._email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or "@" not in value:
            raise ValueError("A valid email address is required.")
        self._email = value

    @email.deleter
    def email(self):
        # Deleting the property clears the optional email value.
        self._email = None


customer = Customer("C001", "meera@example.com")

print("Customer email:", customer.email)

# The deleter is invoked by the del statement.
del customer.email

print("Email after deletion:", customer.email)

# A deleter should not be added merely because Python supports it.
# Consider whether deletion is a valid business operation and whether
# the object remains in a valid state afterward.


# ============================================================
# SECTION 10: BACKING ATTRIBUTES AND NAMING CONVENTIONS
# ============================================================

print("\n--- SECTION 10: BACKING ATTRIBUTES ---")

# A common convention is to use a leading underscore for an internal
# backing attribute, such as _amount.
#
# The public property is amount.
# The backing attribute stores the actual value.
#
# This separation prevents the property getter from calling itself.

class SafeAmount:
    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        # Read the backing attribute, not self.amount.
        return self._amount

    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("Amount must be positive.")
        # Store the value in the backing attribute.
        self._amount = value


safe_amount = SafeAmount(400)
print("Amount:", safe_amount.amount)

# Incorrect recursive getter:
#
#     @property
#     def amount(self):
#         return self.amount
#
# This calls the same property again and again, eventually causing
# RecursionError.
#
# Incorrect recursive setter:
#
#     @amount.setter
#     def amount(self, value):
#         self.amount = value
#
# This assignment invokes the setter again, causing recursion.
#
# Correct pattern:
#     getter -> return self._amount
#     setter -> self._amount = value


# ============================================================
# SECTION 11: PROPERTY VALIDATION AND FAILURE SAFETY
# ============================================================

print("\n--- SECTION 11: FAILURE-SAFE PROPERTY UPDATES ---")

# Validate a proposed value before changing the stored value.
# If validation fails, the existing valid state should remain unchanged.
#
# This is especially important when an object represents financial state.

class Transfer:
    def __init__(self, transfer_id, amount):
        self.transfer_id = transfer_id
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Transfer amount must be numeric.")
        if value <= 0:
            raise ValueError("Transfer amount must be positive.")

        # Assignment occurs only after validation succeeds.
        self._amount = float(value)


transfer = Transfer("TRF001", 2500)
print("Initial transfer amount:", transfer.amount)

try:
    transfer.amount = -900
except ValueError as error:
    print("Rejected update:", error)

# The invalid assignment did not overwrite the existing amount.
print("Amount after rejected update:", transfer.amount)

# Engineering principle:
# Validate first, then mutate.
# Avoid partially updating several related attributes before all
# relevant validation has succeeded.


# ============================================================
# SECTION 12: PROPERTY OR METHOD? DESIGN DECISIONS
# ============================================================

print("\n--- SECTION 12: PROPERTY OR METHOD? ---")

# Use a property when access represents retrieving an attribute-like value.
# Use a method when the caller is asking the object to perform an action,
# especially when the operation has meaningful parameters or side effects.
#
# These are design guidelines, not rigid rules.

class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self._balance = balance

    @property
    def balance(self):
        # Reading the current balance is attribute-like.
        return self._balance

    def deposit(self, amount):
        # Depositing money is an action that changes state.
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    def calculate_interest(self, annual_rate):
        # A parameterised calculation is naturally represented as a method.
        if annual_rate < 0:
            raise ValueError("Annual rate cannot be negative.")
        return self._balance * annual_rate


account = Account("ACC001", 10000)

print("Balance property:", account.balance)
account.deposit(1500)
print("Balance after deposit:", account.balance)
print("Interest estimate:", account.calculate_interest(0.05))

# Avoid hiding a significant state-changing operation behind property
# assignment or access. Callers should be able to recognise actions.


# ============================================================
# SECTION 13: SIDE EFFECTS AND EXPENSIVE PROPERTY CALCULATIONS
# ============================================================

print("\n--- SECTION 13: PROPERTY SIDE EFFECTS ---")

# Property access looks like ordinary attribute access.
# Therefore, callers generally expect it to be simple, predictable
# and reasonably inexpensive.
#
# A property that performs network calls, database queries, writes files
# or changes important state can surprise callers.
#
# Keep property getters free of significant side effects where possible.

class PaymentBatch:
    def __init__(self, payments):
        self.payments = payments

    @property
    def total_amount(self):
        # A straightforward in-memory calculation.
        return sum(self.payments)


batch = PaymentBatch([1000, 2500, 750])

print("Batch total:", batch.total_amount)

# For an expensive report, a method may communicate the cost more clearly:
#
#     batch.generate_reconciliation_report()
#
# Do not use a property simply because a calculation can be written
# without arguments. Consider what callers reasonably expect.


# ============================================================
# SECTION 14: PROPERTY ACCESS AND DESCRIPTOR BEHAVIOUR
# ============================================================

print("\n--- SECTION 14: PROPERTY ACCESS AND DESCRIPTOR BEHAVIOUR ---")

# A property is implemented using Python's descriptor protocol.
# A descriptor is an object that customises attribute access.
#
# At this stage, focus on the practical behaviour:
#     - reading the property invokes its getter
#     - assigning to the property invokes its setter, if defined
#     - deleting the property invokes its deleter, if defined
#
# The property object is defined on the class, while its getter usually
# reads or updates state belonging to a particular instance.

class DescriptorExample:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        print("Getter executed")
        return self._value

    @value.setter
    def value(self, new_value):
        print("Setter executed")
        self._value = new_value


example = DescriptorExample(10)

print("Reading:")
current_value = example.value

print("Assigning:")
example.value = 20

print("Reading again:")
print(example.value)

# The printed messages help reveal when the getter and setter execute.
# The descriptor protocol itself will be studied more deeply only if
# needed for later engineering work; do not confuse this example with
# implementing a custom descriptor.


# ============================================================
# SECTION 15: COMMON PROPERTY IMPLEMENTATION MISTAKES
# ============================================================

print("\n--- SECTION 15: COMMON PROPERTY MISTAKES ---")

# MISTAKE 1: RECURSIVE GETTER
#
#     @property
#     def amount(self):
#         return self.amount
#
# Why incorrect?
# Reading self.amount invokes the same getter again.
# Use a backing attribute such as self._amount.
#
# MISTAKE 2: RECURSIVE SETTER
#
#     @amount.setter
#     def amount(self, value):
#         self.amount = value
#
# Why incorrect?
# Assigning self.amount invokes the same setter again.
# Assign to self._amount after validation.
#
# MISTAKE 3: MISSING BACKING ATTRIBUTE INITIALISATION
#
#     class Payment:
#         @property
#         def amount(self):
#             return self._amount
#
# If _amount is never assigned, accessing amount raises AttributeError.
#
# MISTAKE 4: VALIDATING ONLY IN THE CONSTRUCTOR
#
# If callers can later assign to the public attribute directly,
# constructor-only validation does not protect later updates.
# Use a property setter or another controlled update method.
#
# MISTAKE 5: VALIDATING AFTER MUTATION
#
# Do not overwrite the existing valid value and then discover that
# the new value is invalid. Validate first.
#
# MISTAKE 6: OVERUSING PROPERTIES
#
# A property is not automatically better than a public attribute.
# Simple data containers may not need validation or computed access.
# Add the abstraction when it provides a real benefit.
#
# MISTAKE 7: ASSUMING UNDERSCORE MEANS PRIVATE
#
# _amount is a naming convention signalling internal use.
# It does not prevent callers from accessing or changing it.
#
# MISTAKE 8: HIDING EXPENSIVE OR SURPRISING OPERATIONS
#
# A property getter should not unexpectedly perform network calls,
# database writes or other substantial side effects.


# ============================================================
# SECTION 16: TESTING PROPERTIES
# ============================================================

print("\n--- SECTION 16: TESTING PROPERTIES ---")

# Properties should be tested like other behaviour.
# Tests should cover:
#     - expected getter values
#     - valid setter updates
#     - invalid setter inputs
#     - preservation of previous state after failed updates
#     - read-only behaviour
#
# The following checks use plain assert statements.
# A later testing topic will develop pytest, fixtures and test structure.

class TestedPayment:
    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Amount must be numeric.")
        if value <= 0:
            raise ValueError("Amount must be positive.")
        self._amount = float(value)


tested_payment = TestedPayment(1000)

# Test 1: getter returns the initial value.
assert tested_payment.amount == 1000.0

# Test 2: a valid setter update changes the value.
tested_payment.amount = 1500
assert tested_payment.amount == 1500.0

# Test 3: an invalid update raises the expected exception.
try:
    tested_payment.amount = -1
except ValueError:
    pass
else:
    raise AssertionError("A negative amount should have been rejected.")

# Test 4: failed validation preserves the previous valid value.
assert tested_payment.amount == 1500.0

# Test 5: a boolean is rejected even though bool is a subclass of int.
try:
    tested_payment.amount = True
except TypeError:
    pass
else:
    raise AssertionError("A boolean amount should have been rejected.")

print("Property behaviour checks passed.")


# ============================================================
# SECTION 17: PREDICTION EXERCISES
# ============================================================

"""
Predict every output before running. Explain WHY.

-----------------------------------------
EXERCISE 1 — COMPUTED PROPERTY
-----------------------------------------
class Employee:
    def __init__(self, monthly_salary):
        self.monthly_salary = monthly_salary

    @property
    def annual_salary(self):
        return self.monthly_salary * 12

employee = Employee(50000)
print(employee.annual_salary)
employee.monthly_salary = 60000
print(employee.annual_salary)

Questions:
1. What are the two outputs?
2. Why does the second value change without assigning annual_salary?


-----------------------------------------
EXERCISE 2 — PROPERTY GETTER
-----------------------------------------
class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        print("Getter called")
        return self._balance

account = Account(1000)
value = account.balance
print(value)

Questions:
1. When is the getter executed?
2. How many times is "Getter called" printed?


-----------------------------------------
EXERCISE 3 — PROPERTY SETTER
-----------------------------------------
class Payment:
    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("Invalid amount")
        self._amount = value

payment = Payment(500)
payment.amount = 800
print(payment.amount)

Questions:
1. Does assigning self.amount in __init__ invoke the setter?
2. What is printed?


-----------------------------------------
EXERCISE 4 — INVALID UPDATE
-----------------------------------------
payment = Payment(500)
payment.amount = -100

Questions:
1. What happens during assignment?
2. Is _amount changed to -100?
3. Which line raises the exception?


-----------------------------------------
EXERCISE 5 — READ-ONLY PROPERTY
-----------------------------------------
class Customer:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

customer = Customer("Meera")
print(customer.name)
customer.name = "Ananya"

Questions:
1. Does the first statement succeed?
2. What happens during the assignment?
3. Why?


-----------------------------------------
EXERCISE 6 — RECURSIVE GETTER
-----------------------------------------
class Account:
    @property
    def balance(self):
        return self.balance

account = Account()
print(account.balance)

Questions:
1. Does the getter return a value?
2. What happens and why?
3. How should the getter be corrected?


-----------------------------------------
EXERCISE 7 — PROPERTY OR METHOD?
-----------------------------------------
class Loan:
    def __init__(self, principal):
        self.principal = principal

    @property
    def outstanding_principal(self):
        return self.principal

    def estimate_payment(self, months):
        return self.principal / months

loan = Loan(120000)
print(loan.outstanding_principal)
print(loan.estimate_payment(12))

Questions:
1. Why is outstanding_principal accessed without parentheses?
2. Why does estimate_payment use parentheses?
3. What role does the months argument play?


-----------------------------------------
EXERCISE 8 — DELETER
-----------------------------------------
class Customer:
    def __init__(self, email):
        self._email = email

    @property
    def email(self):
        return self._email

    @email.deleter
    def email(self):
        self._email = None

customer = Customer("a@example.com")
del customer.email
print(customer.email)

Question:
What value is printed, and which method is invoked by del?


-----------------------------------------
EXERCISE 9 — BOOLEAN VALIDATION
-----------------------------------------
isinstance(True, int)

Questions:
1. What does this expression return?
2. Why might a financial amount validator need to reject bool explicitly?
3. How can you write that check?


-----------------------------------------
EXERCISE 10 — VALIDATION ORDER
-----------------------------------------
class Payment:
    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value
        if value <= 0:
            raise ValueError("Invalid amount")

payment = Payment(1000)
try:
    payment.amount = -10
except ValueError:
    print("Rejected")

print(payment.amount)

Questions:
1. Why is this setter unsafe?
2. What value remains in _amount after the exception?
3. How should the setter be reordered?
"""


# ============================================================
# SECTION 18: DEBUGGING EXERCISES
# ============================================================

"""
Find and correct the defects. Do not simply rewrite the classes.

-----------------------------------------
DEBUG 1 — RECURSIVE GETTER
-----------------------------------------
class Payment:
    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        return self.amount

payment = Payment(1000)

Task:
Explain the recursion and correct the backing attribute.


-----------------------------------------
DEBUG 2 — RECURSIVE SETTER
-----------------------------------------
class Payment:
    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self.amount = value

payment = Payment(1000)

Task:
Explain why the setter repeatedly invokes itself and correct it.


-----------------------------------------
DEBUG 3 — VALIDATION AFTER MUTATION
-----------------------------------------
class Account:
    def __init__(self, balance):
        self.balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value
        if value < 0:
            raise ValueError("Balance cannot be negative")

account = Account(5000)

Task:
1. Assign -100 to balance inside a try/except block.
2. Inspect balance after the exception.
3. Correct the setter so invalid updates preserve the previous state.


-----------------------------------------
DEBUG 4 — MISSING BACKING ATTRIBUTE
-----------------------------------------
class Employee:
    @property
    def annual_salary(self):
        return self._annual_salary

employee = Employee()
print(employee.annual_salary)

Task:
Explain why the property access fails.
Decide whether annual_salary should be stored or computed.


-----------------------------------------
DEBUG 5 — WRONG INTERFACE
-----------------------------------------
class Account:
    @property
    def withdraw(self):
        print("Withdrawal requested")

account = Account()
account.withdraw

Task:
Explain why this interface is misleading.
Redesign withdrawal as an explicit method that accepts an amount.
"""


# ============================================================
# SECTION 19: INDEPENDENT IMPLEMENTATION CHALLENGES
# ============================================================

"""
Do not look up solutions immediately.
Implement, run, inspect and explain your decisions.

CHALLENGE 1 — VALIDATED PAYMENT

Create a Payment class with:
    payment_id
    amount
    currency
    status

Requirements:
    - amount must be numeric and greater than zero
    - bool must not be accepted as an amount
    - use a property and setter for amount
    - preserve the old amount if an update is invalid
    - create at least two objects and test them


CHALLENGE 2 — COMPUTED ACCOUNT INFORMATION

Create a BankAccount class with:
    account_number
    balance
    annual_interest_rate

Implement properties:
    - masked_account_number
    - annual_interest_estimate

Requirements:
    - derive values from source attributes
    - do not store redundant calculated values
    - explain which properties should be read-only


CHALLENGE 3 — CONTROLLED CUSTOMER EMAIL

Create a Customer class with:
    customer_id
    email

Requirements:
    - expose email through a property
    - validate that the value is a string and contains "@"
    - support clearing the email using a property deleter
    - decide what the property should return after deletion
    - test valid and invalid updates


CHALLENGE 4 — LOAN PROPERTY DESIGN

Create a Loan class with:
    principal
    annual_rate
    term_months

Implement:
    - a read-only property for annual interest
    - a read-only property for total simple interest over the term
    - a method for estimating a monthly principal-only payment

Requirements:
    - validate source values
    - distinguish properties from parameterised methods
    - explain the assumptions in the calculations


CHALLENGE 5 — PROPERTY FAILURE SAFETY

Create an Account class with a balance property.

Requirements:
    - reject non-numeric values
    - reject bool
    - reject negative values
    - verify failed updates do not alter the existing balance
    - test zero explicitly and decide whether it is valid for this domain


CHALLENGE 6 — PROPERTY OR PUBLIC ATTRIBUTE?

Design two small classes:
    1. A simple data holder where a public attribute is sufficient.
    2. A class where a property adds meaningful validation or computation.

Explain why a property is justified in the second class but unnecessary
in the first.


CHALLENGE 7 — TEST WITHOUT COPYING THE EXAMPLE

Independently implement a property with:
    - a getter
    - a setter
    - at least two validation rules
    - a read-only derived property

Write assertions for valid behaviour and exception handling.
Do not copy the class definitions from earlier sections.
"""


# ============================================================
# SECTION 20: SELF-CHECKS
# ============================================================

print("\n--- SECTION 20: SELF-CHECKS ---")

# These checks verify representative property behaviour.
# An assertion raises AssertionError if its condition is False.

class _PropertyCheck:
    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Amount must be numeric.")
        if value <= 0:
            raise ValueError("Amount must be positive.")
        self._amount = float(value)

    @property
    def doubled_amount(self):
        return self._amount * 2


_property_check = _PropertyCheck(100)

# Check getter.
assert _property_check.amount == 100.0

# Check setter.
_property_check.amount = 250
assert _property_check.amount == 250.0

# Check computed property.
assert _property_check.doubled_amount == 500.0

# Check that invalid values are rejected.
try:
    _property_check.amount = -1
except ValueError:
    pass
else:
    raise AssertionError("Negative amount was not rejected.")

try:
    _property_check.amount = True
except TypeError:
    pass
else:
    raise AssertionError("Boolean amount was not rejected.")

# Check that failed updates preserve the previous value.
assert _property_check.amount == 250.0

# Check that the computed property reflects the latest valid value.
assert _property_check.doubled_amount == 500.0

print("All property self-checks passed.")


# ============================================================
# END OF FILE
# ============================================================

print("\n--- FILE EXECUTED ---")
print("Complete the prediction exercises and independent challenges.")
