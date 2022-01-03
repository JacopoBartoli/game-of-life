import numpy as np

from model.Observable import Observable
from utils.config import config


class GOLModel(Observable):
    """
    Class that represent the state of the Game of Life Grid.
    """

    def __init__(self):
        super().__init__()

        # The base pattern shown.
        self._base_pattern = config.BASE_PATTERN
        # Size of the GOL grid.
        self._grid_size = config.GRID_SIZE
        # The state of the grid is represented by a matrix of integer, where the values of each element represent the
        # corresponding cell age.
        self._grid = np.zeros(self._grid_size, dtype=np.uint8)
        # Flag that indicates if the simulation is running.
        self._is_running = False
        # Flag that indicates if cell's age need to be shown.
        self._show_age = False
        # The speed of the simulation.
        self._fps = config.SPEED
        # The count of the alive cells.
        self._cells_count = 0
        # The number of step taken.
        self._time = 0

    def get_grid(self) -> np.ndarray:
        return self._grid.copy()

    def get_fps(self) -> int:
        return self._fps

    def get_grid_size(self) -> tuple:
        return self._grid_size

    def is_running(self) -> bool:
        return self._is_running

    def is_show_age(self) -> bool:
        return self._show_age

    def get_cells_count(self) -> int:
        return self._cells_count

    def get_time(self) -> int:
        return self._time

    def get_base_pattern(self) -> str:
        return self._base_pattern

    def set_fps(self, value: int) -> None:
        self._fps = value
        self.notify()

    def set_grid_size(self, rows: int, columns: int) -> None:
        self._grid_size = (rows, columns)
        self.notify()

    def set_grid_state(self, grid: np.ndarray) -> None:
        self._grid = grid
        self.notify()

    def set_running(self, value: bool) -> None:
        self._is_running = value
        self.notify()

    def set_show_age(self, value: bool) -> None:
        self._show_age = value
        self.notify()

    def set_cells_count(self, value: int) -> None:
        self._cells_count = value
        self.notify()

    def update_time(self) -> None:
        self._time += 1
        self.notify()

    def reset_time(self) -> None:
        self._time = 0
        self.notify()

    def set_base_pattern(self, value: str) -> None:
        self._base_pattern = value
        self.notify()


