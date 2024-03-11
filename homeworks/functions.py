"""
В этом модуле хранятся функции для применения МНК
"""

from typing import Optional
from numbers import Real       # раскомментируйте при необходимости

from lsm_project.event_logger.event_logger import EventLogger

from lsm_project.lsm.enumerations import MismatchStrategies
from lsm_project.lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)


PRECISION = 3                   # константа для точности вывода
event_logger = EventLogger()    # для логирования


def get_lsm_description(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> LSMDescription:
    """
    Функции для получения описания рассчитаной зависимости

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: mismatch_strategy - стратегия обработки несовпадения

    :return: структура типа LSMDescription
    """

    global event_logger

    try:
        abscissa = list(abscissa)
        ordinates = list(ordinates)
        if _is_valid_measurments(abscissa+ordinates) or len(abscissa) <= 2 or len(ordinates) <= 2:
            raise ValueError
    except:
        raise TypeError
    
    if len(abscissa) != len(ordinates):
        if mismatch_strategy == MismatchStrategies.FALL:
            raise RuntimeError
        elif mismatch_strategy == MismatchStrategies.CUT:
            abscissa, ordinates = _process_mismatch(abscissa, ordinates)
        else:
            raise ValueError

    lsm_description = _get_lsm_description(abscissa, ordinates)

    return LSMDescription(
        incline=lsm_description.incline,
        shift=lsm_description.shift,
        incline_error=lsm_description.incline_error,
        shift_error=lsm_description.shift_error
    )


def get_lsm_lines(
    abscissa: list[float], ordinates: list[float],
    lsm_description: Optional[LSMDescription] = None
) -> LSMLines:
    """
    Функция для расчета значений функций с помощью результатов МНК

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: lsm_description - описание МНК

    :return: структура типа LSMLines
    """
    if lsm_description not in (None, LSMDescription):
        raise TypeError
    elif lsm_description is None:
        lsm_description = get_lsm_description(abscissa, ordinates)

    a = lsm_description.incline
    b = lsm_description.shift
    d_a = lsm_description.incline_error
    d_b = lsm_description.shift_error

    line_predicted = [a * x + b for x in abscissa]
    line_above = [(a + d_a) * x + b + d_b for x in abscissa]
    line_under = [(a - d_a) * x + b - d_b for x in abscissa]
    
    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=line_predicted,
        line_above=line_above,
        line_under=line_under
    )


def get_report(
    lsm_description: LSMDescription, path_to_save: str = ''
) -> str:
    """
    Функция для формирования отчета о результатах МНК

    :param: lsm_description - описание МНК
    :param: path_to_save - путь к файлу для сохранения отчета

    :return: строка - отчет определенного формата
    """
    global PRECISION
    
    result = f'''
    {"LSM computing result".center(100)}
    [INFO]: incline: {lsm_description.incline};
    [INFO]: shift: {lsm_description.shift};
    [INFO]: incline error: {lsm_description.incline_error};
    [INFO]: shift error: {lsm_description.shift_error};'''
    if path_to_save:
        with open(path_to_save, 'w') as file:
            file.write(result)
    return result


# служебная функция для валидации
def _is_valid_measurments(measurments: list[float]) -> bool:
    return all([Real(el) for el in measurments])


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    global event_logger

    if len(abscissa) > len(ordinates):
        abscissa = abscissa[:len(ordinates) + 1]
    else:
        ordinates = ordinates[:len(abscissa) + 1]
    
    return (abscissa, ordinates)


# служебная функция для получения статистик
def _get_lsm_statistics(
    abscissa: list[float], ordinates: list[float]
) -> LSMStatistics:
    global event_logger, PRECISION

    n = len(abscissa)
    av_x = sum(abscissa) / n # Среднее значение x
    av_y = sum(ordinates) / n # Среднее значения y
    av_x2 = sum([x**2 for x in abscissa])/n # Среднее значения квадратов x
    av_xy = sum([x * y for x, y in zip(abscissa, ordinates)]) / n # Среднее значение произведения x и y

    return LSMStatistics(
        abscissa_mean=av_x,
        ordinate_mean=av_y,
        product_mean=av_xy,
        abs_squared_mean=av_x2
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

    a = (av_xy - av_x * av_y)/(av_x2 - (av_x)**2) # Коэффициент a
    b = av_y - a * av_x # Коэффициент b
    d_y = (sum([y - a * x - b for x, y in zip(abscissa, ordinates)]) / (n - 2))**0.5 # Дисперсия y
    d_a = d_y**2 / (n * (av_x2 - av_x**2)) # Дисперсия a
    d_b = (d_y**2 * av_x2) / (n * (av_x2 - av_x**2)) # Дисперсия b
    return LSMDescription(
        incline=a,
        shift=b,
        incline_error=d_a,
        shift_error=d_b
    )
