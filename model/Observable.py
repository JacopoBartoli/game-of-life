from PyQt5.QtCore import QObject, pyqtSignal


class Observable(QObject):
    """
    Implementation of the Observable of the Observer pattern.
    """
    value_changed = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def observe(self, slot):
        self.value_changed.connect(slot)

    def notify(self):
        self.value_changed.emit(self)