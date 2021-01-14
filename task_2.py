'''
Задание 2
Создайте класс для конвертирования температуры из
Цельсия в Фаренгейт и наоборот.
У класса должно быть два статических метода: для перевода из Цельсия в Фаренгейт и для перевода из Фаренгейта в Цельсий.
Также класс должен считать количество подсчетов температуры и возвращать это значение с помощью статического метода.
'''

from typing import List


class Converter:
    __report: List[float] = []

    def __init__(self, celsius: float):
        self.celsius = celsius
        # self.count += 1
        self.__report.append(celsius)

    def set_cel(self, value):
        self.celsius = value

    def set_far(self, value):
        self.far = value

    def cel_to_far(self) -> float:
        return cls.celsius * 9/5 + 32

    @classmethod
    def get_report(cls) -> List[float]:
        return cls.__report


temp1 = Converter(30.0)
assert temp1.cel_to_far() == 86.0


