"""
MODULE 005 — ASYNC PYTHON & CONCURRENCY
PHASE I | REVISION FILE 005.01
Topic: Why async? | Execution models | Coroutines | await | asyncio.run()

This is a revision and practice file. Read it on mobile; run the examples and
complete the exercises when using a laptop.

Run as a script:
    python 005-01-async-foundations.py

Python: 3.10+

=======================================================================
1. FOUR EXECUTION CONCEPTS
=======================================================================

SEQUENTIAL
One operation completes before the next begins:
    A finishes -> B starts -> B finishes -> C starts

CONCURRENT
Multiple tasks are in progress during overlapping periods. For I/O:
    start A -> A waits
              start B -> B waits
                        start C
Their waiting periods overlap. Concurrency does not necessarily mean that
Python instructions execute at exactly the same instant.

PARALLEL
Two or more operations execute at the same instant, for example on separate
CPU cores. Multiprocessing can enable CPU-bound Python work to run in parallel.

SYNCHRONOUS VS ASYNCHRONOUS
Synchronous code generally waits for an operation to finish before proceeding.
Asynchronous code can suspend while awaiting an operation and allow other
eligible tasks to make progress.

These describe related but different dimensions:
- sequential/concurrent: whether work overlaps in time
- synchronous/asynchronous: how waiting is handled
- parallel: whether execution happens simultaneously

Do not use "parallel" as a synonym for "async".

AI ENGINEERING APPLICABILITY
Async/concurrency is useful when an AI application waits on multiple
independent I/O services:
- LLM APIs
- vector databases
- customer or transaction databases
- document/object storage
- external enrichment APIs

It can reduce total wall-clock waiting when independent requests overlap.
Parallel execution is more relevant to CPU-heavy work such as numerical
computation or CPU-intensive preprocessing. Async alone does not make
CPU-bound Python execute on multiple cores.

=======================================================================
2. SYNCHRONOUS EXAMPLE
=======================================================================
"""

import asyncio
import time


def synchronous_operation(name: str, delay: float) -> str:
    print(f"{name}: started")
    time.sleep(delay)  # Blocks this thread.
    print(f"{name}: completed")
    return name


def demonstrate_sequential_execution() -> None:
    """Three blocking operations run one after another."""
    start = time.perf_counter()
    results = [
        synchronous_operation("A", 0.5),
        synchronous_operation("B", 0.5),
        synchronous_operation("C", 0.5),
    ]
    elapsed = time.perf_counter() - start
    print("Results:", results)
    print(f"Sequential elapsed time: {elapsed:.2f}s")


"""
Expected reasoning: A completes before B starts; B completes before C starts.
Elapsed time is approximately the sum of delays (about 1.5 seconds).

=======================================================================
3. WHAT IS A COROUTINE?
=======================================================================

Normal function:
    def fetch_data():
        return "data"

Calling fetch_data() executes the body and returns its result.

Asynchronous function:
    async def fetch_data():
        return "data"

Calling fetch_data() creates a COROUTINE OBJECT. It does not immediately run
the body to completion.

Terminology:
- coroutine function: function defined with async def
- coroutine object: awaitable work created by calling that function
- Task: asyncio object that schedules and manages a coroutine's execution

A Task normally wraps one coroutine, but not every coroutine needs a separate
Task. A coroutine can be awaited directly.

=======================================================================
4. WHAT DOES await DO?
=======================================================================

await means:
"I need this asynchronous operation to complete before this coroutine
continues. If it must wait, suspend this coroutine and let the event loop run
other eligible tasks."

await does NOT automatically create a separate Task.

=======================================================================
5. asyncio.sleep() — A TEACHING TIMER
=======================================================================

    await asyncio.sleep(2)

- asyncio.sleep(2) is an asynchronous timer operation.
- await suspends the current coroutine until the timer completes.
- It does not block the event-loop thread.
- It simulates waiting; it is NOT an API call or API response.

Compare:
    await asyncio.sleep(2)  # suspends coroutine; event loop can run others
    time.sleep(2)           # blocks the executing thread

In a real application:
    response = await client.get(url)

Here the coroutine awaits a network operation rather than an artificial timer.

=======================================================================
6. IS main() A SPECIAL FUNCTION?
=======================================================================

No. main is a conventional name, not a Python keyword.

    async def main():
        ...

It is asynchronous because it uses async def. It could be named
run_application() instead.

For a simple standalone async program:
    asyncio.run(main())

asyncio.run():
- creates/manages an event loop for this top-level coroutine
- runs it until completion
- closes the event loop afterwards

Do not normally call asyncio.run() inside an already-running event loop,
as in many notebook environments. Use the notebook's existing async support.

=======================================================================
7. IMPORTANT: MULTIPLE await EXPRESSIONS DO NOT MEAN CONCURRENCY
=======================================================================

    async def main():
        customer = await fetch_customer()
        transactions = await fetch_transactions()
        device = await fetch_device()

These calls are SEQUENTIAL:
1. main awaits fetch_customer and waits for it to finish.
2. Then it calls and awaits fetch_transactions.
3. Then it calls and awaits fetch_device.

The fact that all three use await does NOT make them concurrent.

To overlap independent operations, we will later schedule them as Tasks or
use asyncio.gather().

Preview of a concurrent pattern:

    async def main():
        customer_task = asyncio.create_task(fetch_customer())
        transactions_task = asyncio.create_task(fetch_transactions())
        device_task = asyncio.create_task(fetch_device())

        customer = await customer_task
        transactions = await transactions_task
        device = await device_task

All three are scheduled before the first await, so they can make progress
concurrently while the event loop is running. We will study this properly
in the upcoming task-scheduling and gather topics.

=======================================================================
8. COMPLETE SMALL EXAMPLE
=======================================================================
"""


async def simple_coroutine() -> str:
    print("Coroutine body is now running")
    return "Data received"


async def demonstrate_coroutine_object() -> None:
    coroutine = simple_coroutine()
    print("Calling async function created a coroutine object.")
    print("Coroutine type:", type(coroutine).__name__)
    result = await coroutine
    print("Result:", result)


async def fetch_demo_data() -> str:
    print("Fetching data...")
    await asyncio.sleep(1)
    print("Data received.")
    return "Customer data"


async def main_demo() -> None:
    result = await fetch_demo_data()
    print(result)


"""
Expected output from main_demo():
    Fetching data...
    [approximately one second passes]
    Data received.
    Customer data

Execution story:
1. asyncio.run(main_demo()) starts the top-level coroutine.
2. main_demo reaches await fetch_demo_data().
3. fetch_demo_data runs.
4. It reaches await asyncio.sleep(1) and suspends.
5. The timer completes; fetch_demo_data resumes.
6. It returns "Customer data".
7. main_demo resumes and prints the result.

This example demonstrates asynchronous waiting, but only one useful
coroutine. It does NOT demonstrate overlapping multiple tasks.

=======================================================================
9. FIVE CORE TAKEAWAYS
=======================================================================

1. A coroutine can pause and resume.
2. Calling an async def function creates a coroutine object; it does not
   immediately execute the body to completion.
3. A Task schedules and manages a coroutine's execution.
4. await suspends the current coroutine while an asynchronous operation is
   pending; it does not automatically create a separate Task.
5. asyncio.run() runs a top-level coroutine using an event loop in a simple
   standalone program.

Also remember:
- main() is a conventional name, not a special function.
- asyncio.sleep() is an asynchronous timer, not an API response.
- Multiple await expressions written one after another are sequential unless
  the operations have already been scheduled to overlap.
- Async is concurrency, not automatically parallelism.

=======================================================================
10. RETRIEVAL QUESTIONS — ANSWER BEFORE RUNNING
=======================================================================

Q1. Difference between a coroutine function and a coroutine object?
Q2. Does calling an async function immediately execute its body?
Q3. Is every coroutine automatically a Task?
Q4. Does await create a new Task?
Q5. Does asyncio.sleep(2) block the event-loop thread?
Q6. Are three consecutive await calls sequential or concurrent? Why?
Q7. Why is "async means parallel" inaccurate?
Q8. Name two I/O-bound AI application operations where async may help.

=======================================================================
11. LAPTOP PRACTICE
=======================================================================

A — Sequential timing
1. Run demonstrate_sequential_execution().
2. Change each delay from 0.5 to 1.0 seconds.
3. Predict total elapsed time before running it.

B — Coroutine object
1. Run demonstrate_coroutine_object() using asyncio.run().
2. Observe that the coroutine body runs when awaited.
3. Explain the difference between creating and executing the coroutine.

C — Async waiting
1. Run asyncio.run(main_demo()) in a normal Python script.
2. Change the sleep duration.
3. Explain what sleep simulates and what await does.

D — Independent explanation
Without looking at this file, explain:
- sequential vs concurrent vs parallel
- synchronous vs asynchronous
- coroutine function vs coroutine object vs Task
- await vs asyncio.sleep()

=======================================================================
12. SUBTOPIC STATUS AND NEXT STEP
=======================================================================

Covered conceptually:
- four execution concepts and AI applicability
- synchronous waiting vs asynchronous waiting
- coroutine function and coroutine object
- Task as scheduler/manager for a coroutine
- await and asynchronous suspension
- asyncio.sleep() as a teaching timer
- main() as a conventional name
- asyncio.run() as a simple program entry mechanism
- sequential awaits versus genuinely concurrent scheduling

Not yet covered in depth:
- event-loop internals
- explicit task creation and task lifecycle
- asyncio.gather()
- exception propagation and timeouts
- HTTPX AsyncClient and remaining VS notebook sections

Next:
Understand how multiple coroutines are scheduled to make progress
concurrently, then study asyncio.gather() as presented in the VS notebook.

This file is not proof of independent coding mastery. Complete the laptop
exercises and ask questions before moving on.
"""


def run_all_demos() -> None:
    print("\\n--- Sequential execution ---")
    demonstrate_sequential_execution()

    print("\\n--- Coroutine object ---")
    asyncio.run(demonstrate_coroutine_object())

    print("\\n--- Single-coroutine async example ---")
    asyncio.run(main_demo())


if __name__ == "__main__":
    run_all_demos()
