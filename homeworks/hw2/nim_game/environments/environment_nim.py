from random import randint

from nim_game.common.models import NimStateChange


STONE_AMOUNT_MIN = 1  # минимальное начальное число камней в кучке
STONE_AMOUNT_MAX = 10  # максимальное начальное число камней в кучке


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]  # кучки

    def __init__(self, heaps_amount: int) -> None:
        if not (2 <= heaps_amount <= 10):
            raise ValueError("invalid heaps amount")

        self._heaps = [
            randint(STONE_AMOUNT_MIN, STONE_AMOUNT_MAX) for _ in range(heaps_amount)
        ]

    def get_state(self) -> list[int]:
        """
        Получение текущего состояния кучек
        :return: копия списка с кучек
        """
        return self._heaps.copy()

    def change_state(self, state_change: NimStateChange) -> None:
        if not (1 <= state_change.heap_id <= len(self._heaps)):
            raise ValueError("invalid number of row")

        if not (1 <= state_change.decrease <= self._heaps[state_change.heap_id - 1]):
            raise ValueError("invalid number of stones")

        self._heaps[state_change.heap_id - 1] -= state_change.decrease
        """
        Изменения текущего состояния кучек
        :param state_change: структура описывающая изменение состояния
        """
