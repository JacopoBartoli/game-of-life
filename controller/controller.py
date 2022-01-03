import math
import os
import numpy as np

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QApplication
from scipy import ndimage

from utils import pattern
from utils.config import config
from gui.main_window import MainWindow
from gui.info_dialog import InfoDialog
from model.gol_model import GOLModel


class Controller:
    """
    Class that connects to the GUI signals to catch the user interactions and modify the GOL state model accordingly.
    """

    def __init__(self, application: QApplication, main_window: MainWindow, gol_model: GOLModel):
        self._application = application

        self._main_window = main_window
        main_window.connect_to_button_clear(self.clear_grid)
        main_window.connect_to_button_load(self.load_custom_pattern)
        main_window.connect_to_button_play(self.start_stop)
        main_window.connect_to_button_save(self.save_pattern)
        main_window.connect_to_button_step(self.single_step)
        main_window.connect_to_combo_patterns(self.select_example_pattern)
        main_window.connect_to_radio_age(self.toggle_show_cell_age)
        main_window.connect_to_slider_speed(self.set_speed)
        main_window.connect_to_dialog(self.display_info)
        main_window.game_grid.connect_to_cell_clicked(self.change_state)

        # Timer for play pause action
        self._timer = QTimer()
        self._timer.timeout.connect(self.single_step)

        self._gol_model = gol_model

        # Variables for the grid update
        self._conv_filter = np.ones((3, 3))
        self._conv_filter[1, 1] = 0

    def clear_grid(self):
        """
        Clear the GOL grid bringing it back to its initial state.
        The initial state is the pattern chosen at the start of the simulation
        :return:
        """
        self.select_example_pattern(self._gol_model.get_base_pattern())
        self._main_window.show_message_on_status_bar("Grid cleared")
        self._gol_model.set_cells_count(0)
        self._gol_model.reset_time()

    def load_custom_pattern(self):
        """
        Load a pattern from a chosen file into the current GOL state
        :return:
        """
        file_path = QFileDialog.getOpenFileName(self._main_window,
                                                "Load pattern ", filter="Pattern File (*.cells)")[0]
        if file_path:
            self._main_window.reset_combo_patterns()
            if self.load_file(file_path):
                self._main_window.show_message_on_status_bar("Pattern loaded")

    def load_file(self, file_path: str) -> bool:
        """
        Method to load a pattern from a .cells file in plain text format
        :param file_path: Path of the pattern file.
        :return: False if the file is invalid or the pattern do not fit the current grid, otherwise True.
        """
        grid_pattern = pattern.read_pattern(file_path)

        if grid_pattern is None:
            self._main_window.show_error_message("Invalid file")
            return False
        else:
            grid_height, grid_width = self._gol_model.get_grid_size()
            pattern_height, pattern_width = grid_pattern.shape

            # Check if the pattern fit in the grid. If not show an error.
            if pattern_height > grid_height or pattern_width > grid_width:
                self._main_window.show_error_message("The loaded pattern is bigger than the available grid")
                return False
            else:
                # Copy the pattern at the center of a blank grid.
                new_grid = np.zeros(self._gol_model.get_grid_size(), np.uint8)
                v_margin = (grid_height - pattern_height) // 2
                h_margin = (grid_width - pattern_width) // 2
                new_grid[v_margin:v_margin + pattern_height, h_margin:h_margin + pattern_width] = grid_pattern

                self._gol_model.set_grid_state(new_grid)
                return True

    def save_pattern(self):
        """
        Save the current grid state in a .cells file as a reloadable state
        :return:
        """
        file_path = QFileDialog.getSaveFileName(self._main_window,
                                                "Save pattern ", filter="Pattern File (*.cells)")[0]
        print("filepath:"+file_path)
        if file_path:
            pattern.save_pattern(file_path + '.cells', self._gol_model.get_grid())
            self._main_window.show_message_on_status_bar("Pattern saved")

    def select_example_pattern(self, pattern_name: str):
        """
        Load a predefined pattern chosen from the provided list
        :param pattern_name: The name of the pattern to load
        :return:
        """
        self._gol_model.set_base_pattern(pattern_name)
        # The selected pattern is the custom one: restart from a blank grid
        if pattern_name == "Custom":
            new_grid = np.zeros(self._gol_model.get_grid_size(), np.uint8)
            self._gol_model.set_grid_state(new_grid)
        else:
            file_path = os.path.join(config.DIR_PATTERN, pattern_name + ".cells")
            if not self.load_file(file_path):
                # If something went wrong during the pattern loading, the custom pattern will be selected.
                self._main_window.reset_combo_patterns()

    def set_speed(self, speed: int):
        """
        Change the simulation's speed
        :param speed: The simulation speed in FPS.
        :return:
        """
        self._gol_model.set_fps(speed)
        if self._gol_model.is_running():
            msec = (1 / self._gol_model.get_fps()) * 1000
            msec = math.floor(msec)
            self._timer.setInterval(msec)

    def single_step(self):
        """
        Performs an update step of the grid applying the Game of Life rules.
        Besides, calculating dead and living cells at the next time step, it also calculates the age of each cell, the
        time since the simulation start and the number of alive cells.
         The age ranges from 0 (dead) to 255 (ancient).
        """
        grid_curr_age = self._gol_model.get_grid()
        grid_curr_alive = grid_curr_age.astype(np.bool).astype(np.uint8)

        # Use convolution to calculate the number of neighbors for each cell.
        grid_neighbors = ndimage.convolve(grid_curr_alive, self._conv_filter, mode="constant", cval=0)

        # Calculate which cells to give birth: a dead cell is born when it has exactly three neighbors.
        grid_newborns = grid_neighbors == 3
        grid_newborns = np.logical_and(grid_newborns, np.logical_not(grid_curr_alive))

        # Calculate which cells survive: a living cell survive when it has two or three neighbors.
        # This is done with the logical AND operator.
        # First it's done between the cells that have 2 or 3 neighbors to calculate the survived cells.
        # Then the logical AND is applied to the current grid and the grid with the survived cells.
        grid_survived = np.logical_and(grid_neighbors >= 2, grid_neighbors <= 3)
        grid_survived = np.logical_and(grid_survived, grid_curr_alive)

        # Calculate the living cells at the next step merging survived and newborn cells, via the logical OR operation.
        grid_next = np.logical_or(grid_newborns, grid_survived).astype(np.uint8)

        # Compute the age of the cells in the new grid, by self addition.
        grid_next = grid_curr_age * grid_next + grid_next
        np.putmask(grid_next, grid_curr_age == 255,
                   255)  # This is necessary to avoid the overflow handling by numpy and cap the array values to 255

        self._gol_model.set_grid_state(grid_next)
        cell_alive = np.count_nonzero(self._gol_model.get_grid())
        self._gol_model.update_time()
        self._gol_model.set_cells_count(cell_alive)

    def start_stop(self):
        """
        Start the GOL simulation or stop it if it was already running
        """
        if not self._gol_model.is_running():
            self._gol_model.set_running(True)
            msec = (1 / self._gol_model.get_fps()) * 1000
            msec = math.floor(msec)
            self._timer.setInterval(msec)
            self._timer.start()
        else:
            self._gol_model.set_running(False)
            self._timer.stop()

    def toggle_show_cell_age(self, show_cell_age: bool):
        self._gol_model.set_show_age(show_cell_age)

    def change_state(self, cell_coord: tuple):
        """
        Change the state of the specified cell
        :param cell_coord: A tuple containing the cell coordinates as (row, column)
        """

        grid = self._gol_model.get_grid()
        row, col = cell_coord
        grid[row, col] = 0 if grid[row, col] else 1
        self._gol_model.set_grid_state(grid)
        cell_alive = np.count_nonzero(self._gol_model.get_grid())
        self._gol_model.set_cells_count(cell_alive)

    def display_info(self):
        """
        Open the dialog that show games information
        :return:
        """
        dialog = InfoDialog(self._main_window)
        dialog.exec()
