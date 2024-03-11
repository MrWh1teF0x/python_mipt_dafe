from typing import Iterable, Union
from numbers import Real

from regressors.regressor_abc import RegressorABC


class RegressorLSM(RegressorABC):
    def fit(self, abscissa: Iterable, ordinates: Iterable) -> None:
        self._abscissa = abscissa
        self._ordinates = ordinates

    def predict(self, abscissa: Union[Real, Iterable]) -> list:
        n = len(abscissa)
        av_x = sum(abscissa) / n
        av_y = sum(self._ordinates) / n
        av_x2 = sum([x**2 for x in abscissa]) / n
        av_xy = sum([x * y for x, y in zip(abscissa, self._ordinates)]) / n
        a = (av_xy - av_x * av_y) / (av_x2 - (av_x) ** 2)
        b = av_y - a * av_x
        return [a * x + b for x in abscissa]
