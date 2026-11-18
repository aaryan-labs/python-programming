"""
Module 004.02 — Database Fundamentals and Basic SQL Operations
AI Engineering Academy | Python Engineering

A practical reference and exercise file for relational database fundamentals,
PostgreSQL schema design, SQL querying, constraints, joins, aggregation,
NULL handling, and basic index trade-offs.

SQL is stored as Python strings so the examples can be studied here and later
executed through a database driver. No database connection is required to
read this file. PostgreSQL execution with psycopg is covered in 004.03.
"""

# 1. RELATIONAL DATABASES
#
# A relational database organizes information into tables.
# Rows represent records; columns represent attributes.
#
# Related entities are stored separately and connected through keys.
# Example:
#   customers (one) ---- (many) accounts
#   accounts  (one) ---- (many) transactions
#
# A primary key uniquely identifies a row in its table.
# A foreign key refers to a key in another table and helps enforce
# referential integrity: a child row cannot refer to a missing parent.

# 2. TABLES, DATA TYPES AND CONSTRAINTS

CREATE_CUSTOMERS = """
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    city VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_ACCOUNTS = """
CREATE TABLE accounts (
    account_id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL
        REFERENCES customers(customer_id),
    account_type VARCHAR(20) NOT NULL
        CHECK (account_type IN ('SAVINGS', 'CURRENT')),
    balance NUMERIC(18, 2) NOT NULL CHECK (balance >= 0),
    opened_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TRANSACTIONS = """
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    account_id BIGINT NOT NULL REFERENCES accounts(account_id),
    amount NUMERIC(18, 2) NOT NULL CHECK (amount > 0),
    status VARCHAR(20) NOT NULL
        CHECK (status IN ('PENDING', 'SUCCESS', 'FAILED')),
    transaction_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

# Common types:
# BIGINT: large whole-number identifiers
# VARCHAR(n) / TEXT: text
# NUMERIC(18, 2): exact decimal arithmetic, suitable for monetary amounts
# BOOLEAN: true/false
# DATE: calendar date
# TIMESTAMPTZ: timestamp with time-zone-aware handling
#
# Prefer NUMERIC/DECIMAL for financial amounts, not FLOAT/REAL/DOUBLE.
# Binary floating-point cannot represent every decimal fraction exactly.
#
# Constraints:
# PRIMARY KEY: unique and not null identifier
# FOREIGN KEY: relationship to another table
# NOT NULL: value is mandatory
# UNIQUE: duplicate non-null values are disallowed
# CHECK: values must satisfy a condition
#
# CHECK does not replace NOT NULL. A CHECK expression evaluating to UNKNOWN
# because a value is NULL does not fail the constraint.

# 3. CRUD: INSERT, SELECT, UPDATE, DELETE

INSERT_CUSTOMER = """
INSERT INTO customers (customer_id, full_name, email, city)
VALUES (101, 'Ravi Kumar', 'ravi@example.com', 'Bengaluru');
"""

SELECT_CUSTOMER = """
SELECT customer_id, full_name, email, city
FROM customers
WHERE customer_id = 101;
"""

UPDATE_CUSTOMER = """
UPDATE customers
SET city = 'Mysuru'
WHERE customer_id = 101;
"""

DELETE_CUSTOMER = """
DELETE FROM customers
WHERE customer_id = 101;
"""

# Caution: UPDATE or DELETE without WHERE affects every row.
# In real applications, verify the predicate and use transactions for
# sensitive changes.

# 4. FILTERING, SORTING AND AGGREGATION

FILTER_AND_SORT = """
SELECT transaction_id, account_id, amount, transaction_timestamp
FROM transactions
WHERE status = 'SUCCESS'
  AND amount >= 10000
ORDER BY transaction_timestamp DESC
LIMIT 20;
"""

CUSTOMER_TRANSACTION_SUMMARY = """
SELECT
    a.customer_id,
    COUNT(*) AS successful_transaction_count,
    SUM(t.amount) AS total_amount
FROM transactions AS t
JOIN accounts AS a ON a.account_id = t.account_id
WHERE t.status = 'SUCCESS'
GROUP BY a.customer_id
HAVING SUM(t.amount) > 50000
ORDER BY total_amount DESC;
"""

# WHERE filters individual rows before grouping.
# GROUP BY forms groups.
# HAVING filters groups after aggregation.
# COUNT(*) counts rows; SUM(column) adds non-NULL values.

# 5. JOINS

INNER_JOIN = """
SELECT a.account_id, c.customer_id, c.full_name, a.balance
FROM accounts AS a
INNER JOIN customers AS c ON c.customer_id = a.customer_id;
"""

LEFT_JOIN = """
SELECT c.customer_id, c.full_name, a.account_id
FROM customers AS c
LEFT JOIN accounts AS a ON a.customer_id = c.customer_id;
"""

# INNER JOIN returns only rows with matches on both sides.
# LEFT JOIN keeps every row from the left table; right-side columns are NULL
# when there is no match.
#
# Use INNER JOIN for customers who have accounts.
# Use LEFT JOIN for all customers, including those without accounts.

# 6. NULL VALUES

FIND_CUSTOMERS_WITHOUT_EMAIL = """
SELECT customer_id, full_name
FROM customers
WHERE email IS NULL;
"""

# NULL is not 0, an empty string, or the text "NULL".
# Use IS NULL / IS NOT NULL, not = NULL.

# 7. INDEXES AND PERFORMANCE

CREATE_TRANSACTION_ACCOUNT_INDEX = """
CREATE INDEX idx_transactions_account_id
ON transactions(account_id);
"""

CREATE_TRANSACTION_STATUS_TIME_INDEX = """
CREATE INDEX idx_transactions_status_timestamp
ON transactions(status, transaction_timestamp);
"""

# An index can help PostgreSQL locate rows without scanning the whole table.
# Indexes consume storage and add work to INSERT/UPDATE/DELETE.
# Do not index every column. Base index choices on query patterns and inspect
# query plans with EXPLAIN (and EXPLAIN ANALYZE when appropriate).

# 8. SQL AND PYTHON: IMPORTANT BOUNDARY
#
# Python code will send SQL to a database using a driver. Never build SQL by
# inserting untrusted values into an f-string.
#
# UNSAFE — do not use:
# sql = f"SELECT * FROM customers WHERE customer_id = {customer_id}"
#
# Parameterized SQL keeps SQL structure separate from data values.
# psycopg placeholder syntax is practised in 004.03.

EXAMPLE_SQL_WITH_PLACEHOLDER = """
SELECT customer_id, full_name
FROM customers
WHERE customer_id = %s;
"""

# 9. GUIDED PRACTICE — ATTEMPT BEFORE READING ANSWERS
#
# Task 1: Return successful transactions >= 25,000, newest first.
# Task 2: Show each account_id, customer name and balance.
# Task 3: Count successful transactions per account.
# Task 4: Explain why NUMERIC(18, 2) is preferable to FLOAT for money.
# Task 5: Explain WHERE versus HAVING using the summary query.

# 10. SUGGESTED ANSWERS

ANSWER_1 = """
SELECT transaction_id, account_id, amount, transaction_timestamp
FROM transactions
WHERE status = 'SUCCESS' AND amount >= 25000
ORDER BY transaction_timestamp DESC;
"""

ANSWER_2 = """
SELECT a.account_id, c.full_name, a.balance
FROM accounts AS a
JOIN customers AS c ON c.customer_id = a.customer_id;
"""

ANSWER_3 = """
SELECT account_id, COUNT(*) AS successful_transaction_count
FROM transactions
WHERE status = 'SUCCESS'
GROUP BY account_id;
"""

# Task 4: NUMERIC stores decimal values exactly within its declared precision
# and scale. Floating-point uses binary approximations.
#
# Task 5: WHERE filters source rows before grouping; HAVING filters groups
# after GROUP BY, often using aggregate expressions.

# 11. INDEPENDENT CHALLENGES
#
# A. Create payment_attempts with:
#    payment_attempt_id primary key
#    transaction_id foreign key to transactions
#    attempt_number positive integer
#    outcome restricted to APPROVED, DECLINED, ERROR
#    attempted_at TIMESTAMPTZ with current-time default
#
# B. Return each customer_id and successful transaction total, including
#    only customers with at least 5 successful transactions and total > 100000.
#
# C. List every customer and any account they own, including customers with
#    no accounts. Choose the appropriate JOIN.
#
# D. A frequent query filters transactions by status and a time range.
#    Propose an index and explain why column order may matter. Validate it
#    using the query plan rather than assuming it helps.

# 12. TOPIC COMPLETION CHECKLIST
#
# [ ] Explain tables, rows, columns and relationships.
# [ ] Distinguish primary keys and foreign keys.
# [ ] Choose suitable basic PostgreSQL data types.
# [ ] Explain NOT NULL, UNIQUE, CHECK and referential integrity.
# [ ] Write basic INSERT, SELECT, UPDATE and DELETE statements.
# [ ] Use WHERE, JOIN, GROUP BY, HAVING and ORDER BY.
# [ ] Distinguish INNER JOIN from LEFT JOIN.
# [ ] Handle NULL values correctly.
# [ ] Explain index purpose and trade-offs.
# [ ] Design and execute a small schema independently.

if __name__ == "__main__":
    print("Module 004.02 — Database Fundamentals")
    print("SQL examples are stored as strings for study and later execution.")
    print("Complete the independent challenges before consulting solutions.")
