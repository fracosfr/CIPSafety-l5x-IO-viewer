from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow

app = QApplication()

w = MainWindow()
w.show()

app.exec()
