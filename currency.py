from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


class Expression(metaclass=ABCMeta):
    @abstractmethod
    def reduce(self, bank: "Bank", to: str) -> "Money":
        pass


class Money(Expression):

    def __init__(self, amount: float, currency: str) -> None:
        self.amount = amount
        self.currency = currency

    def __add__(self, other: object) -> Expression:
        if not isinstance(other, Money):
            return NotImplemented
        return Sum(self, other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money) or self.currency != other.currency:
            return NotImplemented
        return self.amount == other.amount

    def reduce(self, bank: "Bank", to: str) -> "Money":
        rate = bank.rate(self.currency, to)
        return Money(self.amount / rate, to)

    def times(self, multipier: int) -> "Money":
        return Money(self.amount * multipier, self.currency)

    @classmethod
    def dollar(cls, amount: float) -> "Money":
        return Money(amount, "USD")

    @classmethod
    def frank(cls, amount: float) -> "Money":
        return Money(amount, "CHF")


class Sum(Expression):
    def __init__(self, augend: Money, addend: Money) -> None:
        self.augend = augend
        self.addend = addend

    def reduce(self, bank: "Bank", to: str) -> Money:
        amount: float = self.augend.amount + self.addend.amount
        return Money(amount, to)


@dataclass
class Pair:
    base: str
    to: str

    def __hash__(self) -> int:
        return 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pair):
            return NotImplemented
        return self.base == other.base and self.to == other.to


class Bank:
    rates: dict[Pair, int] = {}

    def reduce(self, expression: Expression, to: str) -> Money:
        return expression.reduce(self, to)

    def add_rate(self, base: str, to: str, rate: int) -> None:
        self.rates[Pair(base, to)] = rate

    def rate(self, base: str, to: str) -> int:
        if base == to:
            return 1
        return self.rates.get(Pair(base, to), -1)
