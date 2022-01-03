import sys

from PyQt5.QtWidgets import QApplication

from gui.main_window import MainWindow
from model.gol_model import GOLModel
from controller.controller import Controller

application = QApplication(sys.argv)

# Create model, GUI and controller.
gol_model = GOLModel()
main_window = MainWindow(gol_model)
controller = Controller(application, main_window, gol_model)

main_window.show()
sys.exit(application.exec_())
