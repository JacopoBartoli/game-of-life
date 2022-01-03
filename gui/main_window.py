from PyQt5.QtWidgets import QMainWindow, QMessageBox, QStyle
from gui.game_grid import GameGrid
from gui.ui_main_window import Ui_MainWindow
from model.gol_model import GOLModel
from utils.config import config
from utils import pattern


class MainWindow(QMainWindow):
    """
    Main window of the GUI
    """

    def __init__(self, gol_model: GOLModel):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the icon for the info button.
        api = getattr(QStyle, 'SP_MessageBoxInformation')
        icon = self.style().standardIcon(api)
        self.ui.button_info.setIcon(icon)
        self.ui.button_info.setAutoRaise(True)

        # Set the value of the slider.
        self.ui.slider_speed.setValue(gol_model.get_fps())

        # Add the custom widget to the central QFrame to display the current state of the GOL grid.
        self.game_grid = GameGrid(gol_model)
        self.ui.game_frame.setSpacing(0)
        self.ui.game_frame.addWidget(self.game_grid)

        # Load the available patterns into the QComboBox.
        self.ui.combobox_configurations.insertItem(0, config.BASE_PATTERN)
        self.ui.combobox_configurations.insertItems(1, pattern.get_pattern())

        # Register the UI as observer of the GOLSettingsModel to update the controls with its values.
        self._gol_model = gol_model
        self._gol_model.observe(self.update_controls)
        self._gol_model.observe(self.update_game_state)
        self.update_controls()
        self.update_game_state()

    # Methods to connect slots to the GUI controls signals.
    def connect_to_button_clear(self, slot):
        self.ui.button_clear.clicked.connect(slot)

    def connect_to_button_load(self, slot):
        self.ui.button_load.clicked.connect(slot)

    def connect_to_button_play(self, slot):
        self.ui.button_start.clicked.connect(slot)

    def connect_to_button_save(self, slot):
        self.ui.button_save.clicked.connect(slot)

    def connect_to_button_step(self, slot):
        self.ui.button_singlestep.clicked.connect(slot)

    def connect_to_combo_patterns(self, slot):
        self.ui.combobox_configurations.currentTextChanged.connect(slot)

    def connect_to_radio_age(self, slot):
        self.ui.checkbox_age.toggled.connect(slot)

    def connect_to_slider_speed(self, slot):
        self.ui.slider_speed.valueChanged.connect(slot)

    def connect_to_dialog(self, slot):
        self.ui.button_info.clicked.connect(slot)

    def reset_combo_patterns(self):
        self.ui.combobox_configurations.setCurrentIndex(0)

    def show_error_message(self, message: str):
        """
        Show an error message into a popup dialog
        :param message: The message to show
        """
        QMessageBox.critical(self, "Error", message)

    def show_message_on_status_bar(self, message: str):
        """
        Show a message on the status bar at the bottom of the window
        :param message: The message to show
        """
        self.statusBar().showMessage(message, 2500)

    def update_controls(self):
        """
        Update the controls of the GUI using the current state and settings of the GOL simulation
        """

        # If the simulation is running disable proper controls.
        if self._gol_model.is_running():
            self.ui.button_start.setText("Pause")
            self.ui.button_clear.setEnabled(False)
            self.ui.button_load.setEnabled(False)
            self.ui.button_save.setEnabled(False)
            self.ui.button_singlestep.setEnabled(False)
            self.ui.combobox_configurations.setEnabled(False)
        else:
            self.ui.button_start.setText("Play")
            self.ui.button_clear.setEnabled(True)
            self.ui.button_load.setEnabled(True)
            self.ui.button_save.setEnabled(True)
            self.ui.button_singlestep.setEnabled(True)
            self.ui.combobox_configurations.setEnabled(True)

        self.ui.lbl_fps.setText(f"{self._gol_model.get_fps()} FPS")

    def update_game_state(self):
        self.ui.lbl_time.setText(f"Time: {self._gol_model.get_time()}")
        self.ui.lbl_population.setText(f"Population: {self._gol_model.get_cells_count()}")

