from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtCore import Qt

class CoordinateSystem(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("coordinates X Y")
        self.resize(1080, 1080)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.scene.addLine(-540, 0, 540, 0)
        self.scene.addLine(0, -540, 0, 540)

        self.point = QGraphicsEllipseItem(-5, -5, 10, 10)
        self.point.setBrush(Qt.GlobalColor.red)
        self.scene.addItem(self.point)

        self.setSceneRect(-540, -540, 1080, 1080)
        self.scale(1, -1)

    def set_point(self, x, y):
        scale = 250
        self.point.setPos(x * scale, y * scale)

