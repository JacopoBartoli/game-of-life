from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui

from gui.ui_dialog import Ui_Info
from gui.main_window import MainWindow


class InfoDialog(QDialog):
    """
    Dialog that display the info about the game.
    """

    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.ui = Ui_Info()
        self.ui.setupUi(self)

        self.parent = main_window

        # Link the rule's images.
        self.ui.label_2.setPixmap(QtGui.QPixmap('./resources/images/rule1.png'))
        self.ui.label_5.setPixmap(QtGui.QPixmap("./resources/images/rule4.png"))
        self.ui.label_3.setPixmap(QtGui.QPixmap("./resources/images/rule2.png"))
        self.ui.label_4.setPixmap(QtGui.QPixmap("./resources/images/rule3.png"))
