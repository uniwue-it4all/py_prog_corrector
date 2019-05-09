from typing import Tuple


class Circle:
    def __init__(self, center: Tuple[float, float], radius: float):
        self.center = center
        self.radius = radius

    def __repr__(self) -> str:
        return f'Circle(c = {self.center}, r = {self.radius})'

    def area(self) -> float:
        pass

    def perimeter(self) -> float:
        pass

    def intersects(self, other: 'Circle') -> bool:
        pass
