class L5xModule():
    def __init__(self, operand: str, name: str, values: list) -> None:
        self.operand = operand
        self.name = name
        self.values = values


class L5xAddress():
    def __init__(self, operand: str, name: str) -> None:
        self.operand = operand
        self.name = name
