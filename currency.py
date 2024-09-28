class Dollar:
    def __init__(self, amount: int) -> None:
        self.amount = amount

    def times(self, multipier: int) -> "Dollar":
        return Dollar(self.amount * multipier)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dollar):
            return NotImplemented
        return self.amount == other.amount
