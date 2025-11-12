import sys

from chart import CoordinateSystem2d, CoordinateSystem3d
from ui_mainwindow import MainWindow
from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    chart_window_2d= CoordinateSystem2d()
    chart_window_3d = CoordinateSystem3d()

    main_window.position_changed.connect(chart_window_2d.set_point)

    main_window.show()
    chart_window_3d.show()
    #chart_window_2d.show()

    sys.exit(app.exec())


