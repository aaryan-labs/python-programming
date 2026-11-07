
"""
PYTHON ENGINEERING — MODULE 01
TOPIC 02: NESTED COLLECTIONS AND DEEP COPYING

Learning objectives:
1. Understand nested mutable objects.
2. Understand shallow copying.
3. Understand deep copying.
4. Understand shared references inside collections.
5. Understand list comprehension references.
6. Choose the appropriate copying strategy.

Scenario:
Banking payment batch processing and transaction review.

Run:
    python 02_nested_collections_and_deep_copy.py
"""

import copy

# ============================================================
# SECTION 1: NESTED DATA STRUCTURES
# ============================================================

print("\n--- SECTION 1: NESTED TRANSACTION DATA ---")

transactions = [
    {
        "id": "TXN-101",
        "amount": 500,
        "status": "PROCESSED"
    },
    {
        "id": "TXN-102",
        "amount": 1500,
        "status": "PROCESSED"
    },
    {
        "id": "TXN-103",
        "amount": 5000,
        "status": "PROCESSED"
    }
]

print(transactions)

# Structure:
#
# transactions
#     |
#     +---- List
#             |
#             +---- Dictionary 1
#             |       id
#             |       amount
#             |       status
#             |
#             +---- Dictionary 2
#             |
#             +---- Dictionary 3
#
# A list can contain references to dictionary objects.


# ============================================================
# SECTION 2: ASSIGNMENT OF A NESTED COLLECTION
# ============================================================

print("\n--- SECTION 2: ASSIGNMENT ---")

review_queue = transactions

# No copying occurs.
# Both names refer to the same outer list.

review_queue[0]["amount"] = 750

print("Original:", transactions)
print("Review:", review_queue)

assert transactions[0]["amount"] == 750
assert transactions is review_queue


# ============================================================
# SECTION 3: SHALLOW COPYING
# ============================================================

print("\n--- SECTION 3: SHALLOW COPY ---")

transactions = [
    {"id": "TXN-201", "amount": 500},
    {"id": "TXN-202", "amount": 1500}
]

# Create a new outer list.
# Nested dictionaries remain shared.

review_queue = transactions.copy()

print("Same outer list?", transactions is review_queue)

print(
    "Same first dictionary?",
    transactions[0] is review_queue[0]
)

# Modify a nested dictionary.

review_queue[0]["amount"] = 999

print("Original:", transactions)
print("Review:", review_queue)

# Both show the modified amount!

assert transactions is not review_queue
assert transactions[0] is review_queue[0]
assert transactions[0]["amount"] == 999


# ============================================================
# SECTION 4: MODIFYING THE OUTER LIST
# ============================================================

print("\n--- SECTION 4: OUTER LIST VS NESTED OBJECT ---")

transactions = [
    {"id": "TXN-301", "amount": 500},
    {"id": "TXN-302", "amount": 1000}
]

review_queue = transactions.copy()

# Append a new dictionary to the copied outer list.

review_queue.append(
    {"id": "TXN-303", "amount": 2000}
)

print("Original length:", len(transactions))
print("Review length:", len(review_queue))

# Original list remains unchanged in length.

assert len(transactions) == 2
assert len(review_queue) == 3

# However, modifying an existing nested dictionary
# still affects both collections.

review_queue[0]["amount"] = 800

print("Original first transaction:", transactions[0])
print("Review first transaction:", review_queue[0])

assert transactions[0]["amount"] == 800


# ============================================================
# SECTION 5: DEEP COPYING
# ============================================================

print("\n--- SECTION 5: DEEP COPY ---")

transactions = [
    {
        "id": "TXN-401",
        "amount": 500,
        "metadata": {
            "channel": "UPI",
            "risk_score": 20
        }
    },
    {
        "id": "TXN-402",
        "amount": 2500,
        "metadata": {
            "channel": "CARD",
            "risk_score": 80
        }
    }
]

# deepcopy recursively copies the nested mutable objects.

review_queue = copy.deepcopy(transactions)

print("Same outer list?", transactions is review_queue)

print(
    "Same first dictionary?",
    transactions[0] is review_queue[0]
)

print(
    "Same nested metadata?",
    transactions[0]["metadata"]
    is review_queue[0]["metadata"]
)

# Modify nested data in the copied collection.

review_queue[0]["metadata"]["risk_score"] = 95

print("Original:", transactions[0])
print("Review:", review_queue[0])

# Original remains unchanged.

assert transactions[0]["metadata"]["risk_score"] == 20
assert review_queue[0]["metadata"]["risk_score"] == 95

assert transactions is not review_queue
assert transactions[0] is not review_queue[0]


# ============================================================
# SECTION 6: LIST COMPREHENSION AND REFERENCES
# ============================================================

print("\n--- SECTION 6: LIST COMPREHENSION ---")

transactions = [
    {"id": "TXN-501", "amount": 500},
    {"id": "TXN-502", "amount": 1500},
    {"id": "TXN-503", "amount": 5000}
]

# Select high-value transactions.

high_value = [
    txn
    for txn in transactions
    if txn["amount"] >= 1000
]

print("High-value transactions:", high_value)

# Important:
# The comprehension creates a NEW LIST.
# It does NOT create new dictionary objects.
#
# The selected dictionaries are existing references.

print(
    "Same dictionary?",
    high_value[0] is transactions[1]
)

# Modify through the filtered collection.

high_value[0]["status"] = "REVIEW"

print("Original transaction:", transactions[1])

# The original dictionary is also modified.

assert transactions[1]["status"] == "REVIEW"


# ============================================================
# SECTION 7: INDEPENDENT DICTIONARIES USING COMPREHENSION
# ============================================================

print("\n--- SECTION 7: COPYING SELECTED DICTIONARIES ---")

transactions = [
    {"id": "TXN-601", "amount": 500},
    {"id": "TXN-602", "amount": 2000},
    {"id": "TXN-603", "amount": 5000}
]

# Create a new list AND new dictionaries.
#
# dict(txn) creates a shallow copy of each dictionary.

high_value_copies = [
    dict(txn)
    for txn in transactions
    if txn["amount"] >= 1000
]

print("High-value copies:", high_value_copies)

print(
    "Same dictionary?",
    high_value_copies[0] is transactions[1]
)

high_value_copies[0]["status"] = "REVIEW"

print("Original:", transactions[1])
print("Copy:", high_value_copies[0])

assert "status" not in transactions[1]
assert high_value_copies[0]["status"] == "REVIEW"


# ============================================================
# SECTION 8: SHALLOW COPY VS DEEP COPY COMPARISON
# ============================================================

print("\n--- SECTION 8: COMPARISON ---")

original = [
    {
        "id": "TXN-701",
        "amount": 1000,
        "tags": ["UPI", "HIGH_VALUE"]
    }
]

# Method 1: Assignment.
assigned = original

# Method 2: Shallow copy.
shallow = original.copy()

# Method 3: Deep copy.
deep = copy.deepcopy(original)

print("Assignment:", assigned)
print("Shallow copy:", shallow)
print("Deep copy:", deep)

print("\nIdentity checks:")

print("original is assigned:", original is assigned)
print("original is shallow:", original is shallow)
print("original is deep:", original is deep)

print("\nNested identity checks:")

print(
    "Original dict is shallow dict:",
    original[0] is shallow[0]
)

print(
    "Original tags is shallow tags:",
    original[0]["tags"] is shallow[0]["tags"]
)

print(
    "Original tags is deep tags:",
    original[0]["tags"] is deep[0]["tags"]
)


# ============================================================
# SECTION 9: PRACTICAL PAYMENT REVIEW QUEUE
# ============================================================

print("\n--- SECTION 9: PAYMENT REVIEW APPLICATION ---")

payment_batch = [
    {
        "id": "PAY-001",
        "amount": 500,
        "customer": {
            "name": "Customer A",
            "risk": "LOW"
        }
    },
    {
        "id": "PAY-002",
        "amount": 15000,
        "customer": {
            "name": "Customer B",
            "risk": "HIGH"
        }
    },
    {
        "id": "PAY-003",
        "amount": 2000,
        "customer": {
            "name": "Customer C",
            "risk": "LOW"
        }
    }
]

# We want to create an independent review dataset.
# The original payment batch must remain unchanged.

review_batch = copy.deepcopy(payment_batch)

# Identify high-value payments.

for transaction in review_batch:

    if transaction["amount"] >= 10000:

        transaction["status"] = "REQUIRES_REVIEW"

        transaction["customer"]["risk"] = "MANUAL_CHECK"

print("\nOriginal batch:")
print(payment_batch)

print("\nReview batch:")
print(review_batch)

# Original data must remain unchanged.

assert "status" not in payment_batch[1]
assert payment_batch[1]["customer"]["risk"] == "HIGH"

assert review_batch[1]["status"] == "REQUIRES_REVIEW"
assert review_batch[1]["customer"]["risk"] == "MANUAL_CHECK"


# ============================================================
# SECTION 10: PREDICTION EXERCISES
# ============================================================

"""
-----------
EXERCISE 1:
-----------
a = [{"amount": 100}, {"amount": 200}]
b = a.copy()

b[0]["amount"] = 500

print(a)
print(b)

Why does the original change?

-----------
EXERCISE 2:
-----------
a = [{"amount": 100}, {"amount": 200}]
b = copy.deepcopy(a)

b[0]["amount"] = 500

print(a)
print(b)

Why is the behaviour different?

-----------
EXERCISE 3:
-----------
a = [{"amount": 100}, {"amount": 200}]

b = [x for x in a if x["amount"] >= 100]

b[0]["amount"] = 999

print(a)

Predict the output.

NOTE:
* A new collection does not necessarily mean new objects.
* This applies to list comprehensions, filtering, sorting, slicing and many other Python operations.

-----------
EXERCISE 4:
-----------
a = [{"amount": 100, "metadata": {"channel": "UPI"}}]

b = [dict(x) for x in a]

b[0]["metadata"]["channel"] = "CARD"

print(a)

Will the original nested metadata change?

Try to explain why.
"""


# ============================================================
# SECTION 11: INDEPENDENT ENGINEERING CHALLENGES
# ============================================================

"""
CHALLENGE 1: INDEPENDENT REVIEW QUEUE

Create a payment batch with at least three transactions.

Create an independent review queue.

Modify one transaction's amount in the review queue.

Verify that the original batch remains unchanged.

HINT:
Consider which copying technique you need.


CHALLENGE 2: HIGH-VALUE FILTER

Filter transactions where amount >= 10000.

Create an independent collection of dictionaries.

Modify their review status.

Verify that the original transactions are unchanged.

HINT:
Think about list comprehension combined with copying.


CHALLENGE 3: NESTED CUSTOMER INFORMATION

Each transaction should contain:

{
    "id": "PAY-001",
    "amount": 15000,
    "customer": {
        "name": "Customer A",
        "risk": "HIGH"
    }
}

Create an independent review batch.

Change the nested customer risk classification.

Verify that the original remains unchanged.

HINT:
A shallow dictionary copy is not enough.


CHALLENGE 4: ENGINEERING DECISION

Explain when you would use:

1. Assignment
2. list.copy()
3. dict.copy()
4. copy.deepcopy()
5. A comprehension that creates new dictionaries

Consider memory usage, performance and whether independent nested objects are necessary.
"""

print("\n--- ALL AUTOMATED CHECKS PASSED ---")

# ============================================================
# PYTHON COPYING: QUICK REFERENCE
# ============================================================
#
# 1. ASSIGNMENT
#    new = original
#
#    - No new object is created.
#    - Both variables reference the SAME object.
#    - Mutations through either variable affect the same object.
#
# 2. SHALLOW COPY
#    new = original.copy()
#    new = copy.copy(original)
#
#    - Creates a NEW outer object.
#    - Nested objects are still SHARED.
#    - Mutating the outer collection is independent.
#    - Mutating a shared nested mutable object affects both.
#
# 3. DEEP COPY
#    new = copy.deepcopy(original)
#
#    - Creates a NEW outer object.
#    - Recursively copies nested objects.
#    - Nested mutable objects are independent.
#    - Changes to copied mutable objects do not affect original.
#
# ============================================================
# COMPARISON TABLE
# ============================================================
#
# Feature                 Assignment    Shallow Copy    Deep Copy
# ------------------------------------------------------------
# New outer object?       No            Yes             Yes
# Inner lists shared?     Yes           Yes             No*
# Inner dictionaries
# shared?                 Yes           Yes             No*
# Outer mutation shared?  Yes           No              No
# Inner mutation shared?  Yes           Yes             No*
# Copy depth              None          One level       Recursive
#
# * Deep copy recursively copies nested objects, but immutable
#   objects may be reused. Custom objects may define their own
#   copying behaviour.
#
# ============================================================
# IMPORTANT DISTINCTIONS
# ============================================================
#
# is   -> Checks object identity (same object?)
# ==   -> Checks value equality (equivalent values?)
#
# Shallow copy:
# - Independent outer collection.
# - Shared references to nested objects.
#
# Deep copy:
# - Independent mutable object graph in typical use.
# - Can be more expensive in memory and execution time.
#
# ENGINEERING RULE:
# Choose copying behaviour based on data ownership and
# mutation requirements. Do not deep-copy everything by default.
#
# SUMMARY:
# Assignment shares the object.
# Shallow copy shares nested objects.
# Deep copy recursively copies nested structures
# ============================================================
