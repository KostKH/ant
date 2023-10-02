from typing import Literal

import numpy as np
from memory_profiler import profile
from PIL import Image


class Ant():
    """
    Класс реализует логику поведения муравья.
    При создании экземляра можно задать размер поля
    (size, по-умолчанию 1024x1024), и начальное положение муравья:
    высоту(current_height, по-умолчанию 512) и горизонталь
    (current_width, по-умолчанию 512).
    Для движения муравья вызовите метод `move`. При достижении края поля
    движение муравья прекращается.
    """

    def __init__(
        self,
        size: tuple[int, int] = (1024, 1024),
        current_height: int = 512,
        current_width: int = 512,
    ) -> None:
        self._height_border = size[0] - 1
        self._width_border = size[1] - 1
        self.field = np.full(size, True, dtype='bool_')
        self._current_height = current_height
        self._current_width = current_width
        self._directions = ('left', 'up', 'right', 'down')
        self._direction_index = 1
        self.game_over = False
        self.black_count = 0

    def _change_color(self) -> None:
        """Внутренний метод для изменения цвета поля,
        на котором стоит муравей. Также, идет подсчет клеток черного цвета."""
        if self.field[self._current_height, self._current_width]:
            self.field[self._current_height, self._current_width] = False
            self.black_count += 1
        else:
            self.field[self._current_height, self._current_width] = True
            self.black_count -= 1

    def _change_direction(self) -> None:
        """Метод для смены направления движения муравья.
        Новый индекс направления записывается
        в переменную `_direction_index`."""
        if self.field[self._current_height, self._current_width]:
            self._direction_index = (self._direction_index + 1) % 4
        else:
            self._direction_index = (self._direction_index - 1) % 4

    def _check_borders_are_not_reached(self) -> bool:
        """Метод для проверки, достигнут ли край поля."""
        return (0 < self._current_height < self._height_border
                and 0 < self._current_width < self._width_border)

    def _make_step(self,
                   direction: Literal['up', 'down', 'left', 'right']) -> None:
        """Метод передвигает муравья на один шаг в направлении, указанном
        в параметрах метода."""
        if direction == 'up':
            self._current_height += 1
        elif direction == 'down':
            self._current_height -= 1
        elif direction == 'left':
            self._current_width -= 1
        elif direction == 'right':
            self._current_width += 1

    def move(self) -> None:
        """При вызове метода муравей определяет новое направление,
        меняет цвет текущей клетки, и передвигается на новую клетку, после
        чего проверяет, достигнут ли край поля."""
        if self.game_over:
            return
        self._change_direction()
        self._change_color()
        self._make_step(self._directions[self._direction_index])
        self.game_over = not self._check_borders_are_not_reached()


@profile
def run_game() -> None:
    """Функция создает экземпляр муравья, двигает его до тех пор, пока не
    будет достигнут край поля, после чего сохраняет рисунок пути муравья в
    файл ant_walk.bmp. Функция возвращает экземляр муравья."""
    ant = Ant()
    while not ant.game_over:
        ant.move()
    im = Image.fromarray(ant.field)
    im.save('ant_walk.bmp')
    print(f'Количество черных клеток: {ant.black_count}')


if __name__ == '__main__':
    run_game()
