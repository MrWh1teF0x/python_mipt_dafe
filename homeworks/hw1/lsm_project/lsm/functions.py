"""
В этом модуле хранятся функции для применения МНК
"""

from typing import Optional
from numbers import Real

from lsm_project.event_logger.event_logger import EventLogger

from lsm_project.lsm.enumerations import MismatchStrategies
from lsm_project.lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)


PRECISION = 3  # константа для точности вывода
event_logger = EventLogger()  # для логирования


def get_lsm_description(
    abscissa: list[float],
    ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL,
) -> LSMDescription:
    """
    Функции для получения описания рассчитаной зависимости

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: mismatch_strategy - стратегия обработки несовпадения

    :return: структура типа LSMDescription
    """

    global event_logger

    abscissa = list(abscissa)
    ordinates = list(ordinates)
    _is_valid_measurments(abscissa)
    _is_valid_measurments(ordinates)
    _process_mismatch(abscissa, ordinates, mismatch_strategy)

    lsm_description = _get_lsm_description(abscissa, ordinates)

    return LSMDescription(
        incline=lsm_description.incline,
        shift=lsm_description.shift,
        incline_error=lsm_description.incline_error,
        shift_error=lsm_description.shift_error,
    )


def get_lsm_lines(
    abscissa: list[float],
    ordinates: list[float],
    lsm_description: Optional[LSMDescription] = None,
) -> LSMLines:
    """
    Функция для расчета значений функций с помощью результатов МНК

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: lsm_description - описание МНК

    :return: структура типа LSMLines
    """
    if lsm_description is None:
        lsm_description = get_lsm_description(abscissa, ordinates)
    elif not isinstance(lsm_description, LSMDescription):
        raise TypeError

    a = lsm_description.incline
    b = lsm_description.shift
    a_error = lsm_description.incline_error
    b_error = lsm_description.shift_error

    line_predicted = [a * x + b for x in abscissa]
    line_above = [(a + a_error) * x + b + b_error for x in abscissa]
    line_under = [(a - a_error) * x + b - b_error for x in abscissa]
    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=line_predicted,
        line_above=line_above,
        line_under=line_under,
    )


def get_report(lsm_description: LSMDescription, path_to_save: str = "") -> str:
    """
    Функция для формирования отчета о результатах МНК

    :param: lsm_description - описание МНК
    :param: path_to_save - путь к файлу для сохранения отчета

    :return: строка - отчет определенного формата
    """
    global PRECISION
    result = "\n".join(
        [
            "LSM computing result".center(100, "="),
            "",
            f"[INFO]: incline: {lsm_description.incline:.{PRECISION}f};",
            f"[INFO]: shift: {lsm_description.shift:.{PRECISION}f};",
            f"[INFO]: incline error: {lsm_description.incline_error:.{PRECISION}f};",
            f"[INFO]: shift error: {lsm_description.shift_error:.{PRECISION}f};",
            "",
            "".center(100, "="),
        ]
    )

    if path_to_save != "":
        with open(path_to_save, "w") as file:
            file.write(result)
    return result


# служебная функция для валидации
def _is_valid_measurments(measurments: list[float]) -> bool:
    iter(measurments)
    if not (all([isinstance(el, Real) for el in measurments])):
        raise ValueError
    if len(measurments) <= 2:
        raise ValueError
    return True


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
    abscissa: list[float],
    ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL,
) -> tuple[list[float], list[float]]:
    global event_logger

    if len(abscissa) != len(ordinates):
        if mismatch_strategy == MismatchStrategies.FALL:
            raise RuntimeError
        elif mismatch_strategy == MismatchStrategies.CUT:
            if len(abscissa) > len(ordinates):
                abscissa = abscissa[: len(ordinates)]
            else:
                ordinates = ordinates[: len(abscissa)]
        else:
            raise ValueError
    return [abscissa], [ordinates]


# служебная функция для получения статистик
def _get_lsm_statistics(abscissa: list[float], ordinates: list[float]) -> LSMStatistics:
    global event_logger, PRECISION

    n = len(abscissa)
    av_x = sum(abscissa) / n
    av_y = sum(ordinates) / n
    av_x2 = sum([x**2 for x in abscissa]) / n
    av_xy = sum([x * y for x, y in zip(abscissa, ordinates)]) / n

    return LSMStatistics(
        abscissa_mean=av_x,
        ordinate_mean=av_y,
        product_mean=av_xy,
        abs_squared_mean=av_x2,
    )


# служебная функция для получения описания МНК
def _get_lsm_description(
    abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    global event_logger, PRECISION

    statistics = _get_lsm_statistics(abscissa, ordinates)

    n = len(abscissa)
    av_x = statistics.abscissa_mean
    av_y = statistics.ordinate_mean
    av_xy = statistics.product_mean
    av_x2 = statistics.abs_squared_mean
    a = (av_xy - av_x * av_y) / (av_x2 - (av_x) ** 2)
    b = av_y - a * av_x
    y_error = (
        sum([(y - a * x - b) ** 2 for x, y in zip(abscissa, ordinates)]) / (n - 2)
    ) ** 0.5
    a_error = ((y_error**2) / (n * (av_x2 - av_x**2))) ** 0.5
    b_error = ((y_error**2 * av_x2) / (n * (av_x2 - av_x**2))) ** 0.5

    with open("data_base.txt", "w") as file:
        file.write(f"average x: {av_x}\n\n")
        file.write(f"average y: {av_y}\n\n")
        file.write(f"average xy: {av_xy}\n\n")
        file.write(f"average x^2: {av_x2}\n\n")
        file.write(f"a: {a}\n\n")
        file.write(f"b: {b}\n\n")
        file.write(f"a_error: {a_error}\n\n")
        file.write(f"b_error: {b_error}\n\n")
        file.write(f"y_error: {y_error}\n\n")

    return LSMDescription(
        incline=a, shift=b, incline_error=a_error, shift_error=b_error
    )
