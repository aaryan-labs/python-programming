
"""
PYTHON ENGINEERING — MODULE 01
TOPIC 01: LIST REFERENCES, IDENTITY AND COPYING

Learning objectives:
1. Understand variable names and object references.
2. Understand assignment versus copying.
3. Distinguish identity (is) from equality (==).
4. Understand mutable and immutable objects.
5. Understand list.copy() and independent lists.

Scenario: Banking payment transaction processing.

Run:
    python 01_list_references_and_copying.py
"""

# ============================================================
# SECTION 1: VARIABLES AND OBJECT REFERENCES
# ============================================================

print("\n--- SECTION 1: OBJECT REFERENCES ---")

transactions = [1000, 2000, 3000]

# A variable is a name bound to an object.
# The list is an object; transactions is its reference.

print("Transactions:", transactions)
print("Object identity:", id(transactions))

# Assigning one variable to another does NOT create a new list.

review_queue = transactions

print("Review queue:", review_queue)
print("Same object?", transactions is review_queue)


# ============================================================
# SECTION 2: MUTATING A SHARED OBJECT
# ============================================================

print("\n--- SECTION 2: SHARED MUTATION ---")

# Both names refer to the same list.
# Therefore, modifying through either name affects the same object.

review_queue.append(4000)

print("Transactions:", transactions)
print("Review queue:", review_queue)

assert transactions == [1000, 2000, 3000, 4000]
assert transactions is review_queue


# ============================================================
# SECTION 3: CREATING AN INDEPENDENT LIST
# ============================================================

print("\n--- SECTION 3: SHALLOW LIST COPY ---")

transactions = [1000, 2000, 3000]

# copy() creates a new outer list.

review_queue = transactions.copy()

print("Transactions:", transactions)
print("Review queue:", review_queue)

print("Same object?", transactions is review_queue)
print("Same values?", transactions == review_queue)

# Modify the copied list.

review_queue.append(4000)

print("After modifying review_queue:")
print("Transactions:", transactions)
print("Review queue:", review_queue)

assert transactions == [1000, 2000, 3000]
assert review_queue == [1000, 2000, 3000, 4000]


# ============================================================
# SECTION 4: IDENTITY VS EQUALITY
# ============================================================

print("\n--- SECTION 4: IDENTITY VS EQUALITY ---")

a = [10, 20, 30]

b = a.copy()
c = a

# Change b independently.
b.append(40)

# Change the shared object through c.
c.append(50)

print("a:", a)
print("b:", b)
print("c:", c)

print("a is b:", a is b)
print("a is c:", a is c)

print("a == b:", a == b)
print("a == c:", a == c)

# Expected:
# a = [10, 20, 30, 50]
# b = [10, 20, 30, 40]
# c = [10, 20, 30, 50]
#
# a is b -> False
# a is c -> True
# a == b -> False
# a == c -> True

assert a is not b
assert a is c
assert a != b
assert a == c


# ============================================================
# SECTION 5: MUTABLE VS IMMUTABLE OBJECTS
# ============================================================

print("\n--- SECTION 5: MUTABILITY ---")

# Lists are mutable: their contents can be changed.

payment_amounts = [500, 1000, 1500]

payment_amounts[0] = 750

print("Modified amounts:", payment_amounts)

# Integers are immutable.
# An operation involving an integer produces a new integer value.
# The original integer object is not modified.

amount = 500

another_amount = amount

another_amount = another_amount + 100

print("Original amount:", amount)
print("Another amount:", another_amount)

assert amount == 500
assert another_amount == 600


# ============================================================
# SECTION 6: REASSIGNMENT VS MUTATION
# ============================================================

print("\n--- SECTION 6: REASSIGNMENT ---")

x = [10, 20]
y = x

# Mutation: modifies the shared list.
y.append(30)

print("After mutation:")
print("x:", x)
print("y:", y)

# Reassignment: binds y to a different list object.
y = [100, 200]

print("After reassignment:")
print("x:", x)
print("y:", y)

assert x == [10, 20, 30]
assert y == [100, 200]
assert x is not y


# ============================================================
# SECTION 7: PRACTICAL BANKING APPLICATION
# ============================================================

print("\n--- SECTION 7: PAYMENT REVIEW QUEUE ---")

# Original batch received from an upstream system.

payment_batch = [
    500,
    1200,
    3000,
    750,
    5000
]

# Create a separate list for review.
review_batch = payment_batch.copy()

# Flag high-value payments.
review_batch.append(10000)

print("Original payment batch:", payment_batch)
print("Review batch:", review_batch)

# Original data remains unchanged.

assert len(payment_batch) == 5
assert len(review_batch) == 6


# ============================================================
# SECTION 8: PREDICTION EXERCISES
# ============================================================

"""
Before running these examples, predict their outputs.

EXERCISE 1:

p = [10, 20]
q = p
r = p.copy()

q.append(30)
r.append(40)

print(p)
print(q)
print(r)

EXERCISE 2:

a = [1, 2, 3]
b = a

b = [4, 5, 6]

print(a)
print(b)
print(a is b)

EXERCISE 3:

x = 100
y = x

y += 50

print(x)
print(y)

EXERCISE 4:

a = [1, 2, 3]
b = a.copy()

print(a == b)
print(a is b)

Try to explain WHY, not just predict the output.
"""


# ============================================================
# SECTION 9: INDEPENDENT PRACTICE
# ============================================================

"""
CHALLENGE 1:
Create a list of five transaction amounts.
Assign it to another variable.
Append a transaction through the second variable.
Observe the original list.

CHALLENGE 2:
Create an independent copy.
Change an element in the copied list.
Verify that the original is unchanged.

CHALLENGE 3:
Create two separate lists with identical values.
Test both identity and equality.

CHALLENGE 4:
Explain the difference between:
    a = original
    a = original.copy()

HINT:
Think about whether Python creates a new object.

Do not look up solutions immediately.
Predict, implement and inspect the results.
"""

print("\n--- ALL AUTOMATED CHECKS PASSED ---")
