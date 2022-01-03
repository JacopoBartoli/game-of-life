import math

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget

from model.gol_model import GOLModel
from utils.utils import np_to_qimage


class GameGrid(QLabel):

    changeCellState = pyqtSignal(object)

    def __init__(self, model: GOLModel):
        super().__init__()

        # Set the game grid policies.
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(1, 1)
        self.setStyleSheet("border: 0px;")

        # Coordinates of the pixmap.
        self.x_pixmap = 0
        self.y_pixmap = 0

        # Keep track of the last tile drawn to handle continuous drawing through mouse dragging.
        self._last_drawn_row = -1
        self._last_drawn_col = -1
        # Flag that indicates whether we are drawing on the grid.
        self._drawing = False

        self._gol_model = model
        self._gol_model.observe(self.update_grid)
        self.update_grid()

        QWidget.setMouseTracking(self, True)

    def connect_to_cell_clicked(self, slot) -> None:
        self.changeCellState.connect(slot)

    def update_grid(self) -> None:
        """
        Method that update the QImage representing the grid.
        :return:
        """

        # Transform the numpy array of the grid in to an image.
        image = np_to_qimage(self._gol_model.get_grid(), self._gol_model.is_show_age())
        pixmap = QPixmap.fromImage(image)

        self.setPixmap(pixmap.scaled(self.width(), self.height()))

        self.x_pixmap = (self.width() - self.pixmap().width()) // 2
        self.y_pixmap = (self.height() - self.pixmap().height()) // 2

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        Slot for the resize event of the widget. It updates the QPixmap coordinates to handle mouse events on the grid
        and repaints the new grid
        :param event: The resize event.
        :return:
        """
        self.x_pixmap = (self.width() - self.pixmap().width()) // 2
        self.y_pixmap = (self.height() - self.pixmap().height()) // 2
        self.update_grid()

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        """
        Slot for the mouse move event on the widget.
        When the application is in a drawing session, change the state of all the cells where the mouse pass over
        :param ev: The mouse event.
        :return:
        """
        x_pos = ev.pos().x()
        y_pos = ev.pos().y()

        # Check if the mouse position is inside the grid image.
        x_grid = x_pos - self.x_pixmap
        y_grid = y_pos - self.y_pixmap
        if 0 <= x_grid < self.pixmap().width() and 0 <= y_grid < self.pixmap().height() and \
                not self._gol_model.is_running():
            self.setCursor(Qt.CrossCursor)

            # Check if we are drawing (the mouse is pressed and dragged).
            if self._drawing:
                # Converts the widget coordinates into grid coordinates.
                grid_size = self._gol_model.get_grid_size()
                row = math.floor(y_grid * grid_size[0] / self.pixmap().height())
                col = math.floor(x_grid * grid_size[1] / self.pixmap().width())

                # Check if the event was already handled for this tile.
                if row != self._last_drawn_row or col != self._last_drawn_col:
                    self.changeCellState.emit((row, col))
                    self._last_drawn_row = row
                    self._last_drawn_col = col
        else:
            self.unsetCursor()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        """
        Slot for the mouse press event on the widget. It allows the user to edit the grid cells only when the simulation
        is not running.
        Emits the changeCellState signal sending to the connected slots the coordinates (row, column) of the clicked
        cell and starts a drawing session
        :param ev: The mouse event.
        :return:
        """

        # Ignore the mouse click if the simulation is running (the grid is not editable).
        if not self._gol_model.is_running():
            x_click = ev.pos().x()
            y_click = ev.pos().y()

            # Converts the widget coordinates into grid coordinates
            x_grid = x_click - self.x_pixmap
            y_grid = y_click - self.y_pixmap
            if 0 <= x_grid < self.pixmap().width() and 0 <= y_grid < self.pixmap().height():
                # Converts the widget coordinates into grid coordinates
                grid_size = self._gol_model.get_grid_size()
                row = math.floor(y_grid * grid_size[0] / self.pixmap().height())
                col = math.floor(x_grid * grid_size[1] / self.pixmap().width())

                self.changeCellState.emit((row, col))
                self._last_drawn_row = row
                self._last_drawn_col = col

                # Start continuous drawing
                self._drawing = True

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        """
        Slot for the mouse release event on the widget.
        Ends the drawing session
        :param ev: The mouse event.
        :return:
        """

        self._drawing = False
        self._last_drawn_row = -1
        self._last_drawn_col = -1
