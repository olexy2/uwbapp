import sys

from chart import CoordinateSystem
from ui_mainwindow import MainWindow
from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    chart_window = CoordinateSystem()

    main_window.position_changed.connect(chart_window.set_point)

    main_window.show()
    chart_window.show()

    sys.exit(app.exec())


