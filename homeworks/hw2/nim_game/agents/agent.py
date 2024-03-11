from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels  # уровень сложности

    def __init__(self, level: str) -> None:
        level = AgentLevels(level)
        if not (level in AgentLevels):
            raise ValueError("invalid level")
        self._level = level

    def get_xor_sum(self, state_curr: list[int]) -> int:
        summa = 0
        for i in range(len(state_curr)):
            summa ^= state_curr[i]
        return summa

    def easy_step(self, state_curr: list[int]) -> NimStateChange:
        accept_rows = []

        for i in range(len(state_curr)):
            if state_curr[i] != 0:
                accept_rows.append(i)

        row_curr = choice(accept_rows)
        return NimStateChange(row_curr, randint(1, state_curr[row_curr]))

    def hard_step(self, state_curr: list[int]) -> NimStateChange:
        accept_rows = []

        for i in range(len(state_curr)):
            for n in range(1, state_curr[i] + 1):
                accept_rows.append(i)

                temp = state_curr.copy()
                temp[i] -= n
                res = self.get_xor_sum(temp)
                if res == 0:
                    return NimStateChange(i, n)

        return NimStateChange(choice(accept_rows), 1)

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """

        if self._level == AgentLevels.NORMAL:
            what_lvl = AgentLevels.EASY if randint(0, 1) == 1 else AgentLevels.HARD

            if what_lvl == AgentLevels.EASY:
                return self.easy_step(state_curr)
            return self.hard_step(state_curr)

        elif self._level == AgentLevels.EASY:
            return self.easy_step(state_curr)

        elif self._level == AgentLevels.HARD:
            return self.hard_step(state_curr)
