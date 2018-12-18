from typing import Tuple


class Circle:
    def __init__(self, center: Tuple[float, float], radius: float):
        self.center = center
        self.radius = radius
        pass

    def __repr__(self) -> str:
        # i = 0
        # while True:
        #     i = i + 1
        pass

    def area(self) -> float:
        pass

    def perimeter(self) -> float:
        pass

    def intersects(self, other: 'Circle') -> bool:
        pass
