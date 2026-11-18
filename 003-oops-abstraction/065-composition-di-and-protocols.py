"""
PYTHON ENGINEERING — MODULE 003
FILE 065: COMPOSITION, DEPENDENCY INJECTION AND PROTOCOLS

STUDY SEQUENCE
1. Read the explanation before each code block.
2. Predict the output or behaviour before running the block.
3. Run the file from top to bottom.
4. Change one thing at a time and observe the effect.
5. Complete the independent challenges without copying the examples.

PURPOSE
Build a small, replaceable payment-risk enrichment component. The focus is
Python object composition, dependency injection and structural interfaces.
This is deliberately a component, not a framework or a complete payment
processing platform.

ENGINEERING OUTCOMES
- Explain why composition is often preferable to inheritance.
- Inject dependencies instead of constructing infrastructure internally.
- Define a provider-independent contract with typing.Protocol.
- Replace a real-looking provider with a deterministic fake.
- Test behaviour at component boundaries.
"""

from dataclasses import dataclass
from typing import Protocol


# ============================================================
# SECTION 1: THE PROBLEM — A COMPONENT THAT KNOWS TOO MUCH
# ============================================================

# A common design mistake is allowing domain logic to construct and own
# an external service directly. The class below is tightly coupled to one
# concrete risk provider.
#
# If the provider changes, tests become harder and this class must change.
# It also mixes two responsibilities:
#   1. deciding what risk score means for the application;
#   2. deciding how to contact a particular external provider.


class RiskProviderA:
    """A stand-in for an external risk-scoring service."""

    def score(self, customer_id: str, amount: float) -> int:
        # A deterministic stand-in keeps this learning file executable.
        # A real implementation might call an HTTP API.
        return 72


class TightlyCoupledRiskChecker:
    def __init__(self) -> None:
        # The dependency is created inside the class.
        # Callers cannot easily replace it with another provider or a fake.
        self._provider = RiskProviderA()

    def is_high_risk(self, customer_id: str, amount: float) -> bool:
        score = self._provider.score(customer_id, amount)
        return score >= 70


checker = TightlyCoupledRiskChecker()
print("Tightly coupled result:", checker.is_high_risk("C-100", 2500.0))


# ============================================================
# SECTION 2: COMPOSITION — BUILD OBJECTS FROM COLLABORATORS
# ============================================================

# Composition means an object holds references to other objects and
# delegates parts of its work to them.
#
# Inheritance expresses an "is-a" relationship and reuses/extends behaviour
# through a class hierarchy. Composition expresses a "has-a/uses-a"
# relationship and allows collaborators to be replaced independently.
#
# A risk checker does not need to BE a provider. It USES a provider.
#
# The constructor accepts the collaborator. This is constructor injection,
# a straightforward form of dependency injection.


class ConfigurableRiskChecker:
    def __init__(self, provider) -> None:
        self._provider = provider

    def is_high_risk(self, customer_id: str, amount: float) -> bool:
        score = self._provider.score(customer_id, amount)
        return score >= 70


checker_a = ConfigurableRiskChecker(RiskProviderA())
print("Composed result:", checker_a.is_high_risk("C-100", 2500.0))


# ============================================================
# SECTION 3: DEPENDENCY INJECTION — WHO CREATES THE DEPENDENCY?
# ============================================================

# Dependency injection does not require a framework or container.
# The essential idea is that a component receives the collaborator it needs
# rather than secretly creating that collaborator itself.
#
# The composition root is the place where the application chooses and
# assembles concrete implementations. For this small example, the lines
# that instantiate the provider and checker form the composition root.
#
# Benefits:
#   - tests can inject a fake;
#   - a different provider can be selected without rewriting domain logic;
#   - object construction and business decisions remain separate.
#
# Trade-off:
#   - the caller now has responsibility for assembling valid collaborators;
#   - injecting every trivial value can make code unnecessarily indirect.


class RiskProviderB:
    """A second provider with different internal implementation."""

    def score(self, customer_id: str, amount: float) -> int:
        # Different rule, same operation expected by the checker.
        return 35 if amount < 5000 else 88


provider = RiskProviderB()                  # Select infrastructure.
checker_b = ConfigurableRiskChecker(provider)  # Inject the dependency.
print("Provider B result:", checker_b.is_high_risk("C-200", 2500.0))


# ============================================================
# SECTION 4: DUCK TYPING — BEHAVIOUR MATTERS
# ============================================================

# Python often uses duck typing: code can work with an object because it
# supports the required operations, not because it inherits from a
# particular base class.
#
# ConfigurableRiskChecker calls provider.score(...). It does not need to
# know the provider's concrete class.
#
# This is flexible, but an undocumented expectation can be unclear.
# typing.Protocol lets us describe the expected shape for static analysis.


class MinimalProvider:
    def score(self, customer_id: str, amount: float) -> int:
        return 10


duck_checker = ConfigurableRiskChecker(MinimalProvider())
print("Duck-typed result:", duck_checker.is_high_risk("C-300", 100.0))


# ============================================================
# SECTION 5: typing.Protocol — A STRUCTURAL CONTRACT
# ============================================================

# Protocol describes the operations a collaborator must provide.
# A class does not have to inherit from RiskScorer to satisfy this protocol.
# This is structural subtyping: compatibility is based on the available
# members and their types, rather than an explicit inheritance relationship.
#
# Protocol improves documentation and static type checking. It does not
# automatically validate arbitrary runtime objects or make network calls safe.


class RiskScorer(Protocol):
    def score(self, customer_id: str, amount: float) -> int:
        """Return an integer risk score for the supplied customer and amount."""


class ProtocolRiskChecker:
    def __init__(self, provider: RiskScorer, threshold: int = 70) -> None:
        self._provider = provider
        self._threshold = threshold

    def is_high_risk(self, customer_id: str, amount: float) -> bool:
        score = self._provider.score(customer_id, amount)
        return score >= self._threshold


typed_checker = ProtocolRiskChecker(RiskProviderB(), threshold=65)
print("Protocol-based result:", typed_checker.is_high_risk("C-400", 7000.0))


# ============================================================
# SECTION 6: A FAKE IMPLEMENTATION FOR DETERMINISTIC TESTS
# ============================================================

# A fake is a simple, working implementation used to control a dependency
# during a test. Unlike a mock, a fake usually contains a small amount of
# functional behaviour.
#
# This fake records calls as well as returning a configured score. Tests
# can verify both the result and the interaction at the boundary.


class FakeRiskScorer:
    def __init__(self, score_to_return: int) -> None:
        self.score_to_return = score_to_return
        self.calls: list[tuple[str, float]] = []

    def score(self, customer_id: str, amount: float) -> int:
        self.calls.append((customer_id, amount))
        return self.score_to_return


low_risk_fake = FakeRiskScorer(20)
high_risk_fake = FakeRiskScorer(95)

low_checker = ProtocolRiskChecker(low_risk_fake)
high_checker = ProtocolRiskChecker(high_risk_fake)

assert low_checker.is_high_risk("C-500", 1200.0) is False
assert high_checker.is_high_risk("C-501", 1200.0) is True
assert low_risk_fake.calls == [("C-500", 1200.0)]
assert high_risk_fake.calls == [("C-501", 1200.0)]

print("Fake-based checks passed.")


# ============================================================
# SECTION 7: VALIDATE DOMAIN INPUTS AT THE RIGHT BOUNDARY
# ============================================================

# A Protocol describes a collaborator's behaviour; it does not validate
# business input. Keep those responsibilities separate.
#
# This small immutable dataclass is a domain value object. It validates
# invariants that must hold whenever a RiskRequest is created.
#
# For this exercise, amount is represented as float to keep attention on
# composition. In real financial systems, prefer Decimal or integer minor
# units and define currency/rounding rules explicitly.


@dataclass(frozen=True)
class RiskRequest:
    customer_id: str
    amount: float

    def __post_init__(self) -> None:
        if not self.customer_id.strip():
            raise ValueError("customer_id must not be blank")
        if self.amount <= 0:
            raise ValueError("amount must be positive")


class RiskAssessmentService:
    def __init__(self, scorer: RiskScorer, threshold: int = 70) -> None:
        self._scorer = scorer
        self._threshold = threshold

    def assess(self, request: RiskRequest) -> bool:
        score = self._scorer.score(request.customer_id, request.amount)
        if not 0 <= score <= 100:
            raise ValueError("risk score must be between 0 and 100")
        return score >= self._threshold


service_fake = FakeRiskScorer(82)
service = RiskAssessmentService(service_fake)
request = RiskRequest(customer_id="C-600", amount=4500.0)

assert service.assess(request) is True
assert service_fake.calls == [("C-600", 4500.0)]
print("Validated domain request:", request)


# ============================================================
# SECTION 8: ERROR HANDLING — DEFINE THE COMPONENT'S BOUNDARY
# ============================================================

# External providers can fail. A component should not silently convert
# every failure into "low risk", because that can turn an outage into an
# unsafe approval decision.
#
# This example translates an infrastructure exception into a domain-level
# failure. The policy for what the application does next (retry, hold,
# reject, manual review) belongs to a higher-level use case.
#
# Do not catch Exception indiscriminately in every method. Catch the
# failures you can meaningfully handle or translate.


class RiskProviderUnavailable(RuntimeError):
    """Raised when a risk provider cannot produce an assessment."""


class UnavailableRiskScorer:
    def score(self, customer_id: str, amount: float) -> int:
        raise TimeoutError("risk provider timed out")


class SafeRiskAssessmentService:
    def __init__(self, scorer: RiskScorer, threshold: int = 70) -> None:
        self._scorer = scorer
        self._threshold = threshold

    def assess(self, request: RiskRequest) -> bool:
        try:
            score = self._scorer.score(request.customer_id, request.amount)
        except TimeoutError as exc:
            # Preserve the original exception as the cause for debugging.
            raise RiskProviderUnavailable("risk assessment unavailable") from exc

        if not 0 <= score <= 100:
            raise ValueError("risk score must be between 0 and 100")
        return score >= self._threshold


unavailable_service = SafeRiskAssessmentService(UnavailableRiskScorer())
try:
    unavailable_service.assess(request)
except RiskProviderUnavailable as exc:
    print("Expected boundary failure:", exc)


# ============================================================
# SECTION 9: COMPOSITION VERSUS INHERITANCE — DESIGN CHECK
# ============================================================

# Consider these questions before choosing inheritance:
#   1. Is the new type genuinely a specialised kind of the parent type?
#   2. Can it honour the parent's behavioural expectations?
#   3. Does the relationship need shared implementation, or just a contract?
#
# Prefer composition when an object collaborates with a service, repository,
# clock, policy or provider. Prefer Protocol when the caller needs a small
# behavioural contract without forcing a shared class hierarchy.
#
# Inheritance remains useful when there is a genuine substitutable "is-a"
# relationship. It is not inherently wrong.


# ============================================================
# SECTION 10: PREDICTION EXERCISES — DO NOT RUN FIRST
# ============================================================

# PREDICTION 1
# What does this print?
#
# fake = FakeRiskScorer(69)
# component = ProtocolRiskChecker(fake, threshold=70)
# print(component.is_high_risk("C-700", 99.0))
# print(fake.calls)
#
# PREDICTION 2
# Does this class need to inherit from RiskScorer to be accepted by a
# type checker as a RiskScorer?
#
# class LocalScorer:
#     def score(self, customer_id: str, amount: float) -> int:
#         return 50
#
# Explain structural subtyping in your own words.
#
# PREDICTION 3
# What happens if RiskRequest is constructed with amount=0?
# Which method enforces the rule, and when does it run?
#
# PREDICTION 4
# Why is returning False after a provider timeout potentially dangerous?
# State one explicit fail-safe policy an application might choose.


# ============================================================
# SECTION 11: INDEPENDENT IMPLEMENTATION CHALLENGE
# ============================================================

# Do not copy the preceding service line by line.
#
# Implement a TransactionEnrichmentService with these requirements:
#
# 1. Define a Protocol named TransactionEnricher.
#    It must declare:
#        enrich(transaction_id: str, customer_id: str) -> dict[str, object]
#
# 2. Implement a dataclass named EnrichmentRequest.
#    transaction_id and customer_id must be non-empty strings.
#
# 3. Implement TransactionEnrichmentService.
#    Inject a TransactionEnricher through its constructor.
#    Do not instantiate a concrete enricher inside the service.
#
# 4. Add a fake enricher that:
#    - returns a configurable dictionary;
#    - records every call;
#    - can be used without network access.
#
# 5. Write assertions proving:
#    - the service delegates to the injected object;
#    - the expected input values reach the enricher;
#    - a second enricher implementation can be substituted;
#    - invalid request data is rejected.
#
# 6. Add one failure case. Decide whether the service should translate the
#    failure or allow a documented domain exception to propagate.
#
# 7. Explain why composition and Protocol are appropriate here, and why
#    subclassing a concrete provider would create unnecessary coupling.
#
# Keep the implementation small. Do not build a plugin registry, abstract
# factory framework, generic dependency container or unrelated architecture.


# ============================================================
# SECTION 12: SELF-CHECK AND TOPIC RETRIEVAL
# ============================================================

# You should be able to explain, without reading the earlier sections:
#
# [ ] Composition versus inheritance.
# [ ] Constructor injection and the composition root.
# [ ] Duck typing versus nominal inheritance.
# [ ] Structural subtyping and typing.Protocol.
# [ ] Why Protocol does not perform runtime input validation.
# [ ] How a fake supports deterministic boundary tests.
# [ ] Why provider failure must not silently become a low-risk result.
# [ ] One trade-off introduced by dependency injection.
#
# TOPIC CLOSURE EVIDENCE
# This file alone does not establish mastery. Closure requires you to:
# - explain the concepts accurately;
# - complete the independent challenge without copying;
# - test normal, invalid and provider-failure paths;
# - substitute a second implementation;
# - defend the design trade-offs.
#
# Suggested next step after this file:
# Review your implementation for single responsibility, dependency
# inversion, interface size and unnecessary abstraction.
