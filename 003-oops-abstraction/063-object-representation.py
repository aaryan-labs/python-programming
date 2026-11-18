"""
PYTHON ENGINEERING — MODULE 003
TOPIC 03: OBJECT REPRESENTATION — __str__ AND __repr__

Run:
    python 063-object-representation.py

Study sequence:
1. Read one section at a time.
2. Understand the explanation comments before running the code.
3. Predict outputs where a prediction is requested.
4. Run the examples and inspect the results.
5. Complete the independent challenges.
6. Explain WHY, not just WHAT.

Scenario: Banking payment processing.
"""


# ============================================================
# SECTION 1: WHY OBJECT REPRESENTATION MATTERS
# ============================================================

print("\n--- SECTION 1: WHY OBJECT REPRESENTATION MATTERS ---")

# In earlier topics, we created classes and instantiated objects.
# For example, a Payment object stores payment_id, amount and status.
#
# When we print a built-in value such as an integer or string, Python
# already knows how to display that value in a useful way.
#
# However, when we print an instance of our own class, Python does not
# automatically know which business details we want to see.
#
# Without a custom representation, the output usually contains:
#     - the class name
#     - information identifying the object in the current process
#
# This default output does not tell us the payment ID, amount or status.
# That makes it less useful when inspecting objects during development.

class Payment:
    def __init__(self, payment_id, amount, status):
        # Store the business data belonging to this Payment instance.
        self.payment_id = payment_id
        self.amount = amount
        self.status = status


# Create one Payment object so that we can inspect its default display.
payment = Payment("TXN001", 1500, "SETTLED")

print("Default object representation:")
print(payment)

# Observe:
# The output identifies the object as an instance of Payment.
# It does not provide a useful summary of the payment's business data.
#
# Python provides special methods that allow a class to define how its
# instances should be represented as strings:
#     __str__  -> readable representation
#     __repr__ -> developer-oriented representation


# ============================================================
# SECTION 2: __str__ — A READABLE REPRESENTATION
# ============================================================

print("\n--- SECTION 2: __str__ ---")

# __str__ is a special method used to define a readable string
# representation of an object.
#
# It is commonly used when:
#     - print(object) is executed
#     - str(object) is called
#
# The representation should communicate the important information
# about the object in a clear and readable form.
#
# In this Payment example, a user or operations analyst may want to see:
#     payment ID | amount | payment status
#
# Notice that __str__ RETURNS a string. It does not print the string.
# The caller decides whether to display it, store it or use it elsewhere.

class Payment:
    def __init__(self, payment_id, amount, status):
        self.payment_id = payment_id
        self.amount = amount
        self.status = status

    def __str__(self):
        # Build and return a readable summary of this Payment instance.
        # self refers to the particular Payment object being represented.
        return (
            f"Payment {self.payment_id}: "
            f"₹{self.amount:,.2f} ({self.status})"
        )

payment = Payment("TXN002", 2500, "SETTLED")

# print(payment) asks Python for the object's readable string.
print("Using print():")
print(payment)

# str(payment) explicitly requests the same readable representation.
# We can also store the returned string in a variable.
payment_text = str(payment)

print("Using str():")
print(payment_text)

# Important:
# __str__ must return an object of type str.
# Printing inside __str__ is not a substitute for returning a string.
#
# The distinction between print and return was covered in File 062:
#     print() displays a value.
#     return sends a value back to the caller.


# ============================================================
# SECTION 3: __repr__ — A DEVELOPER-ORIENTED REPRESENTATION
# ============================================================

print("\n--- SECTION 3: __repr__ ---")

# __repr__ defines the official or developer-oriented representation
# of an object.
#
# It is particularly useful when:
#     - inspecting an object during debugging
#     - examining objects in an interactive Python session
#     - inspecting objects contained inside collections
#
# A useful __repr__ should make the object's state clear and,
# where practical, provide an unambiguous representation.
#
# A common convention is to make the output resemble a constructor call.
# This can help a developer understand which values were used to describe
# the object.
#
# In the f-string below, !r applies repr() to the value being formatted.
# For string values, this generally includes quotes in the representation.

class Payment:
    def __init__(self, payment_id, amount, status):
        self.payment_id = payment_id
        self.amount = amount
        self.status = status

    def __repr__(self):
        # Return a developer-oriented representation of the object.
        # !r requests the representation of each attribute value.
        return (
            f"Payment(payment_id={self.payment_id!r}, "
            f"amount={self.amount!r}, "
            f"status={self.status!r})"
        )

payment = Payment("TXN003", 3750, "PENDING")

# repr(payment) explicitly requests the developer representation.
payment_representation = repr(payment)

print("Using repr():")
print(payment_representation)

# Observe:
# The representation includes the attribute names and their values.
# This makes it easier to inspect the state of the object.


# ============================================================
# SECTION 4: DEFINING BOTH __str__ AND __repr__
# ============================================================

print("\n--- SECTION 4: DEFINING BOTH METHODS ---")

# A class can define both __str__ and __repr__.
#
# They serve different purposes:
#     __str__  -> concise, readable representation
#     __repr__ -> informative, developer-oriented representation
#
# For a payment object, a concise summary may be convenient for an
# operations screen, while a more explicit representation may be useful
# when debugging code.
#
# Both methods describe the SAME object. They simply present its state
# in different formats.

class Payment:
    def __init__(self, payment_id, amount, status):
        self.payment_id = payment_id
        self.amount = amount
        self.status = status

    def __str__(self):
        # A concise representation suitable for ordinary display.
        return (
            f"{self.payment_id} | "
            f"₹{self.amount:,.2f} | "
            f"{self.status}"
        )

    def __repr__(self):
        # A more explicit representation useful during development.
        return (
            f"Payment(payment_id={self.payment_id!r}, "
            f"amount={self.amount!r}, "
            f"status={self.status!r})"
        )


payment = Payment("TXN004", 4200, "SETTLED")

# print(object) normally uses the object's __str__ implementation.
print("print(payment):")
print(payment)

# repr(object) explicitly requests the object's __repr__ implementation.
print("repr(payment):")
print(repr(payment))

# Compare the two outputs.
# Both describe TXN004, but the formatting and intended audience differ.


# ============================================================
# SECTION 5: WHAT HAPPENS WHEN __str__ IS NOT DEFINED?
# ============================================================

print("\n--- SECTION 5: WHEN __str__ IS NOT DEFINED ---")

# A class does not have to define both methods.
#
# If __str__ is not defined, Python can fall back to __repr__ when
# a string representation is requested.
#
# This means that print(customer) can still produce a useful output
# when Customer defines __repr__ but does not define __str__.
#
# This is useful when a developer wants to provide a meaningful
# representation without implementing two separate methods.

class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name

    def __repr__(self):
        # There is deliberately no __str__ method in this class.
        return (
            f"Customer(customer_id={self.customer_id!r}, "
            f"name={self.name!r})"
        )


customer = Customer("C001", "Meera")

# Since Customer does not define __str__, str(customer) falls back
# to the available __repr__ implementation.
print("Using print(customer):")
print(customer)

print("Using str(customer):")
print(str(customer))

print("Using repr(customer):")
print(repr(customer))

# Observe:
# The three calls produce the same representation in this example,
# because the class has __repr__ but no custom __str__.


# ============================================================
# SECTION 6: OBJECTS INSIDE COLLECTIONS
# ============================================================

print("\n--- SECTION 6: OBJECTS INSIDE COLLECTIONS ---")

# Consider a payment-processing application that handles many payments.
# We may store Payment objects in a list for further processing.
#
# When we print one Payment object directly, Python requests its
# readable representation through __str__.
#
# When we print a list containing Payment objects, Python displays
# the representation of each element in the list.
#
# For list elements, Python uses repr() rather than str().
# This is why implementing __repr__ is particularly useful when
# inspecting collections of custom objects.

class Payment:
    def __init__(self, payment_id, amount, status):
        self.payment_id = payment_id
        self.amount = amount
        self.status = status

    def __str__(self):
        # Readable representation for one payment.
        return (
            f"{self.payment_id}: "
            f"₹{self.amount:,.2f} "
            f"[{self.status}]"
        )

    def __repr__(self):
        # Developer representation used when the object is an element
        # inside a collection such as a list.
        return (
            f"Payment(payment_id={self.payment_id!r}, "
            f"amount={self.amount!r}, "
            f"status={self.status!r})"
        )


# Create three different Payment instances.
payments = [
    Payment("TXN101", 1000, "SETTLED"),
    Payment("TXN102", 2500, "PENDING"),
    Payment("TXN103", 750, "FAILED"),
]

# Printing one object directly uses its __str__ method.
print("Printing one Payment object:")
print(payments[0])

# Printing the list uses the __repr__ representation of each element.
print("Printing the complete list:")
print(payments)

# If we iterate over the list and print each object individually,
# each print(item) uses that object's __str__ method.
print("Printing each Payment individually:")
for item in payments:
    print(item)

# Compare the output of print(payments) with the loop output.
# This distinction is important when debugging collections of objects.


# ============================================================
# SECTION 7: __repr__ IS NOT THE SAME AS SERIALIZATION
# ============================================================

print("\n--- SECTION 7: REPRESENTATION VERSUS SERIALIZATION ---")

# A constructor-like __repr__ may look similar to executable Python code.
# However, its purpose is to represent an object for inspection.
#
# Do not assume that repr(object):
#     - is always valid executable Python
#     - can safely be passed to eval()
#     - is an appropriate format for storing application data
#     - is a suitable API response
#
# Serialization is a separate engineering concern.
# When an application needs to exchange or persist data, define explicitly
# which fields should be converted into a supported data format.
#
# Here, to_dict() returns a dictionary containing the selected fields.
# This is deliberately separate from __repr__.

class Payment:
    def __init__(self, payment_id, amount, status):
        self.payment_id = payment_id
        self.amount = amount
        self.status = status

    def __repr__(self):
        # Useful for inspecting the Payment instance during development.
        return (
            f"Payment(payment_id={self.payment_id!r}, "
            f"amount={self.amount!r}, "
            f"status={self.status!r})"
        )

    def to_dict(self):
        # Return an explicit data structure for further processing.
        # The caller can decide whether and how to serialize this dictionary.
        return {
            "payment_id": self.payment_id,
            "amount": self.amount,
            "status": self.status,
        }


payment = Payment("TXN201", 1800, "SETTLED")

print("Developer representation:")
print(repr(payment))

print("Dictionary representation:")
print(payment.to_dict())

# Notice that repr(payment) and payment.to_dict() serve different purposes.
# One is intended for inspection; the other exposes selected data fields.


# ============================================================
# SECTION 8: COMMON IMPLEMENTATION MISTAKES AND SECURITY
# ============================================================

print("\n--- SECTION 8: COMMON MISTAKES AND SECURITY ---")

# ----------------------------------------
# MISTAKE 1: PRINTING INSTEAD OF RETURNING
# ----------------------------------------
# Incorrect implementation:
#
#     def __str__(self):
#         print(self.payment_id)
#
# Why is this incorrect?
# __str__ is expected to return a string to the caller.
# The print statement only displays the value. It does not return it.
# If __str__ implicitly returns None, str(object) raises TypeError.
#
# Correct pattern:
#
#     def __str__(self):
#         return self.payment_id
# ----------------------------------------
# MISTAKE 2: RETURNING A NON-STRING VALUE
# ----------------------------------------
# Both __str__ and __repr__ must return a str object.
# Returning an integer, list, dictionary or None is not valid.
# -------------------------------------------------
# MISTAKE 3: EXPOSING SENSITIVE PAYMENT INFORMATION
# -------------------------------------------------
# Representations may appear in:
#     - logs
#     - tracebacks
#     - debugging output
#     - monitoring and diagnostic systems
#
# Avoid including sensitive information such as:
#     - full card numbers
#     - CVVs
#     - passwords
#     - authentication tokens
#     - bank-account credentials
#
# A useful representation should help debugging without disclosing secrets.
#
# The following example masks an account identifier.

class PaymentInstrument:
    def __init__(self, instrument_id, account_number):
        self.instrument_id = instrument_id
        self.account_number = account_number

    def __str__(self):
        # Display only the last four digits of the account identifier.
        masked_account = "*" * (len(self.account_number) - 4)
        masked_account += self.account_number[-4:]
        return (
            f"Instrument {self.instrument_id}: "
            f"Account {masked_account}"
        )

    def __repr__(self):
        # Do not expose the full account number in developer output either.
        return (
            f"PaymentInstrument(instrument_id={self.instrument_id!r}, "
            f"account_number='***{self.account_number[-4:]}')"
        )


instrument = PaymentInstrument("PI001", "123456789012")

print("Readable instrument representation:")
print(instrument)

print("Developer instrument representation:")
print(repr(instrument))


# ============================================================
# SECTION 9: PREDICTION EXERCISES
# ============================================================

"""
Predict every output before running. Explain WHY.

-----------------------------------------
EXERCISE 1 — DEFAULT REPRESENTATION
-----------------------------------------
class Transaction:
    def __init__(self, transaction_id, amount):
        self.transaction_id = transaction_id
        self.amount = amount

transaction = Transaction("TXN501", 5000)
print(transaction)

Questions:
1. Will the output display the transaction ID and amount?
2. Why does Python produce this output by default?


-----------------------------------------
EXERCISE 2 — __str__ AND __repr__
-----------------------------------------
class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def __str__(self):
        return f"{self.payment_id}: ₹{self.amount}"

    def __repr__(self):
        return (
            f"Payment(payment_id={self.payment_id!r}, "
            f"amount={self.amount!r})"
        )

payment = Payment("TXN502", 2500)

print(payment)
print(str(payment))
print(repr(payment))

Questions:
1. Which method is used by print(payment)?
2. Which method is requested by repr(payment)?
3. Do both methods represent the same object?


-----------------------------------------
EXERCISE 3 — __STR__ IS NOT DEFINED
-----------------------------------------
class Customer:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Customer(name={self.name!r})"

customer = Customer("Meera")

print(customer)
print(str(customer))
print(repr(customer))

Question:
Why do these calls produce the same representation?


-----------------------------------------
EXERCISE 4 — OBJECTS INSIDE A LIST
-----------------------------------------
class Payment:
    def __init__(self, payment_id):
        self.payment_id = payment_id

    def __str__(self):
        return f"Payment ID: {self.payment_id}"

    def __repr__(self):
        return f"Payment({self.payment_id!r})"

payments = [
    Payment("TXN601"),
    Payment("TXN602")
]

print(payments)
print(payments[0])

Questions:
1. Which method supplies the representation of list elements?
2. Which method is used when printing payments[0] directly?


-----------------------------------------
EXERCISE 5 — PRINT VERSUS RETURN
-----------------------------------------
class Payment:
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        print(f"Payment amount: {self.amount}")

payment = Payment(1000)
print(payment)

Question:
Why does this implementation fail when print(payment) is executed?
What should __str__ do instead?


-----------------------------------------
EXERCISE 6 — REPRESENTATION VERSUS DATA
-----------------------------------------
class Payment:
    def __init__(self, payment_id, amount):
        self.payment_id = payment_id
        self.amount = amount

    def __repr__(self):
        return (
            f"Payment({self.payment_id!r}, {self.amount!r})"
        )

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "amount": self.amount
        }

payment = Payment("TXN701", 7000)

print(repr(payment))
print(payment.to_dict())

Question:
Why are these two outputs different, and what is the purpose of each?
"""


# ============================================================
# SECTION 10: INDEPENDENT IMPLEMENTATION CHALLENGES
# ============================================================

"""
CHALLENGE 1 — TRANSACTION REPRESENTATION

Create a Transaction class with:
    transaction_id
    amount
    currency
    status

Implement:
    __str__  -> concise, readable transaction summary
    __repr__ -> explicit developer-oriented representation

Create two Transaction objects and print both representations.


CHALLENGE 2 — INSPECT A COLLECTION

Create at least three Transaction objects and store them in a list.

Print:
    1. One Transaction object directly.
    2. repr() of one Transaction object.
    3. The complete list.
    4. Every Transaction object individually using a loop.

Explain which representation method is used in each case.


CHALLENGE 3 — FALLBACK BEHAVIOUR

Create a class that defines __repr__ but does not define __str__.

Compare:
    print(object)
    str(object)
    repr(object)

Explain why the outputs are the same.


CHALLENGE 4 — SAFE REPRESENTATION

Create a PaymentInstrument class containing a sensitive account or card
identifier.

Implement __str__ and __repr__ so that neither exposes the full identifier.

Test both methods and inspect the output carefully.


CHALLENGE 5 — REPRESENTATION AND SERIALIZATION

Add a to_dict() method to your Transaction class.

Return selected transaction fields as a dictionary.

Compare:
    repr(transaction)
    transaction.to_dict()

Explain why debugging representation and data serialization are separate
responsibilities.


Do not look up solutions immediately.
Implement, run, inspect and explain your decisions.
"""


# ============================================================
# SECTION 11: SELF-CHECKS
# ============================================================

print("\n--- SECTION 11: SELF-CHECKS ---")

# These assertions verify the essential behaviour covered in this file.
# An assertion raises AssertionError if its condition is False.
# If execution reaches the final print statement, all checks have passed.

class _RepresentationCheck:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Readable({self.value})"

    def __repr__(self):
        return f"_RepresentationCheck(value={self.value!r})"


check_object = _RepresentationCheck("TXN999")

# Verify that str() uses the custom __str__ implementation.
assert str(check_object) == "Readable(TXN999)"

# Verify that repr() uses the custom __repr__ implementation.
assert repr(check_object) == "_RepresentationCheck(value='TXN999')"

# Verify that a list uses repr() for its elements.
assert (
    str([check_object])
    == "[_RepresentationCheck(value='TXN999')]"
)

print("All self-checks passed.")


# ============================================================
# END OF FILE
# ============================================================

print("\n--- FILE EXECUTED ---")
print("Complete the prediction exercises and independent challenges.")
