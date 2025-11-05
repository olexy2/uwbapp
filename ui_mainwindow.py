from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGridLayout, QWidget, QLineEdit, QPushButton, QLabel, QTextEdit, QMessageBox

import serial.tools.list_ports
import tag_lib as tag
import re


class MainWindow(QWidget):

    position_changed = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()

        self.ser = None

        self.setWindowTitle('UWB APP')
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet('background-color: #24272B;')

        self.x_pos = 0,
        self.y_pos = 0,

        #--------------------LABELS/LINE EDIT

        self.distance_line = QLineEdit()
        self.distance_line.setReadOnly(True)
        self._2d_pos_line = QLineEdit()
        self._2d_pos_line.setReadOnly(True)

        self.config_label = QLabel('Configurate UWB Module')
        self.measurements_label = QLabel('Measurements')
        self._2d_pos_label = QLabel('2D positioning')
        self.x_2d_label = QLabel('set anchor X coordinate [mm]')
        self.y_2d_label = QLabel('set anchor Y coordinate [mm]')
        self.x_2d_line = QLineEdit()
        self.y_2d_line = QLineEdit()
        self.serial_port_name_label = QLabel('Serial port name')
        self.baudrate_label = QLabel('Baudrate')
        self.mode_label = QLabel('Mode')
        self.panid_label = QLabel('Personal Area Network ID (hex)')
        self.update_rate_label = QLabel('Update Rate [Hz]')
        self.node_label = QLabel('Node Label')

        self.serial_port_name_line = QLineEdit(self)
        self.baudrate_line = QLineEdit(self)
        self.mode_line = QLineEdit(self)
        self.panid_line = QLineEdit(self)
        self.update_rate_line = QLineEdit(self)
        self.node_label_line = QLineEdit(self)

        self.info_line = QTextEdit()
        self.info_line.setEnabled(0)
        self.terminal_textbox = QTextEdit()
        self.terminal_textbox.setEnabled(0)

        #--------------------BUTTONS

        #--------------------1ST COLUMN
        self.connect_btn = QPushButton('connect')
        self.connect_btn.clicked.connect(self.serial_con_accept)

        self.save_changes_btn = QPushButton('accept') #ACCEPT 1
        self.save_changes_btn.clicked.connect(self.set_mode)

        self.set_panid_btn = QPushButton('accept') #ACCEPT 2
        self.set_panid_btn.clicked.connect(self.set_panid)

        self.update_rate_btn = QPushButton('accept') #ACCEPT 3
        self.update_rate_btn.clicked.connect(self.set_update_rate)

        self.node_label_accept = QPushButton('accept') #ACCEPT 4
        self.node_label_accept.clicked.connect(self.set_node_label)

        self.y_2d_btn = QPushButton('accept X and Y') #ACCEPT 5
        self.y_2d_btn.clicked.connect(self.set_2d_xy)

        self.get_serial_ports_btn = QPushButton('get serial ports')
        self.get_serial_ports_btn.clicked.connect(self.get_serial_ports)

        self.reboot_btn = QPushButton('reboot the module')
        self.reboot_btn.clicked.connect(self.reboot_module)

        self.anchors_list_btn = QPushButton('show anchors in network')
        self.anchors_list_btn.clicked.connect(self.show_anchors_list)

        self.module_mode_btn = QPushButton('show module mode')
        self.module_mode_btn.clicked.connect(self.show_module_mode)

        #--------------------2ND COLUMN

        self.measure_btn = QPushButton('start distance measuring')
        self.measure_btn.clicked.connect(self.start_measure)

        self.stop_meas_btn = QPushButton('stop distance measuring')
        self.stop_meas_btn.clicked.connect(self.stop_measure)

        self._2d_pos_btn_start = QPushButton('start 2D positioning')
        self._2d_pos_btn_start.clicked.connect(self.start_measure_2d)

        self._2d_pos_btn_stop = QPushButton('stop 2D positioning')
        self._2d_pos_btn_stop.clicked.connect(self.stop_measure)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_distance)
        self.timer.setInterval(100)
        self.timer.stop()

        self.build_ui()

    def build_ui(self):
        layout = QGridLayout()
        layout.setVerticalSpacing(5)

        big_font = QFont()
        big_font.setPointSize(32)

        small_font = QFont()
        small_font.setPointSize(12)

        tiny_font = QFont()
        tiny_font.setPointSize(10)

        alignement_top = Qt.AlignmentFlag.AlignTop

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        self.distance_line.setPlaceholderText('distance [m]')
        self._2d_pos_line.setPlaceholderText('[X, Y]')


        self.config_label.setFont(big_font)
        self.config_label.setStyleSheet('color: blue')

        self.measurements_label.setFont(big_font)
        self.measurements_label.setStyleSheet('color: orange')

        self._2d_pos_label.setFont(big_font)
        self._2d_pos_label.setStyleSheet('color: green')

        white_small_font_widgets = [
            self.measure_btn,
            self.stop_meas_btn,
            self.get_serial_ports_btn,
            self.reboot_btn,
            self.anchors_list_btn,
            self.module_mode_btn,
            self.info_line,
            self.connect_btn,
            self.distance_line,
            self._2d_pos_line,
            self._2d_pos_btn_start,
            self._2d_pos_btn_stop,
            self.x_2d_label,
            self.y_2d_label,
            self.x_2d_line,
            self.y_2d_line,
            self.serial_port_name_label,
            self.serial_port_name_line,
            self.baudrate_label,
            self.baudrate_line,
            self.mode_label,
            self.mode_line,
            self.panid_label,
            self.panid_line,
            self.update_rate_label,
            self.update_rate_line,
            self.node_label,
            self.node_label_line,
        ]

        for widget in white_small_font_widgets:
            if isinstance(widget, QPushButton):
                widget.setFont(small_font)
                widget.setStyleSheet('color: white; background-color: #3D3D40;')
            else:
                widget.setFont(small_font)
                widget.setFixedHeight(36)
                widget.setStyleSheet('color: white')

        white_tiny_font_widgets = [
            self.save_changes_btn,
            self.set_panid_btn,
            self.update_rate_btn,
            self.node_label_accept,
            self.y_2d_btn,
        ]

        for widget in white_tiny_font_widgets:
            if isinstance(widget, QPushButton):
                widget.setFont(tiny_font)
                widget.setStyleSheet('color: white; background-color: #3D3D40;')
        #---------------- COLUMN 0
        left_layout = QGridLayout()

        left_layout.addWidget(self.config_label, 0, 0, alignement_top)
        left_layout.addWidget(self.terminal_textbox, 2, 0)

        box_left_layout1 = QGridLayout()

        box_left_layout1.addWidget(self.serial_port_name_label, 0, 0)
        box_left_layout1.addWidget(self.baudrate_label, 1, 0)
        box_left_layout1.addWidget(self.mode_label, 4, 0)
        box_left_layout1.addWidget(self.panid_label, 5, 0)
        box_left_layout1.addWidget(self.update_rate_label, 6, 0)
        box_left_layout1.addWidget(self.node_label, 7, 0)

        box_left_layout1.addWidget(self.connect_btn, 2, 0, 1, 3)
        box_left_layout1.addWidget(self.save_changes_btn, 4, 2)
        box_left_layout1.addWidget(self.set_panid_btn, 5, 2)
        box_left_layout1.addWidget(self.update_rate_btn, 6, 2)
        box_left_layout1.addWidget(self.node_label_accept, 7, 2)
        box_left_layout1.addWidget(self.get_serial_ports_btn, 3, 0, 1, 3)
        box_left_layout1.addWidget(self.reboot_btn, 8, 0)
        box_left_layout1.addWidget(self.anchors_list_btn, 8, 1, 1, 2)
        box_left_layout1.addWidget(self.module_mode_btn, 9, 0)

        box_left_layout1.addWidget(self.serial_port_name_line, 0, 1, 1, 3)
        box_left_layout1.addWidget(self.baudrate_line, 1, 1, 1, 3)
        box_left_layout1.addWidget(self.mode_line, 4, 1)
        box_left_layout1.addWidget(self.panid_line, 5, 1)
        box_left_layout1.addWidget(self.update_rate_line, 6, 1)
        box_left_layout1.addWidget(self.node_label_line, 7, 1)
        box_left_layout1.addWidget(self.info_line, 10, 0, 1, 3)

        layout.addLayout(left_layout, 0, 0)
        left_layout.addLayout(box_left_layout1, 1, 0)

        # ---------------- COLUMN 1
        right_layout = QGridLayout()

        right_layout1 = QGridLayout()
        right_layout1.setContentsMargins(0, 0, 0, 0)

        right_layout1.addWidget(self.measurements_label, 0, 0)
        right_layout1.addWidget(self.distance_line, 1, 0)
        right_layout1.addWidget(self.measure_btn, 2, 0)
        right_layout1.addWidget(self.stop_meas_btn, 3, 0)

        layout.addLayout(right_layout, 0, 1)
        right_layout.addLayout(right_layout1, 1, 0, alignement_top)

        right_layout2 = QGridLayout()
        right_layout2.setContentsMargins(0, 0, 0, 0)
        right_layout2.addWidget(self._2d_pos_label, 4, 0, 1, 3)
        right_layout2.addWidget(self._2d_pos_line, 5, 0, 1, 3)
        right_layout2.addWidget(self._2d_pos_btn_start, 6, 0, 1, 3)
        right_layout2.addWidget(self._2d_pos_btn_stop, 7, 0, 1, 3)
        right_layout2.addWidget(self.x_2d_label, 8, 0, 1, 1)
        right_layout2.addWidget(self.y_2d_label, 9, 0, 1, 1)
        right_layout2.addWidget(self.x_2d_line, 8, 1, 1, 1)
        right_layout2.addWidget(self.y_2d_line, 9, 1, 1, 1)
        right_layout2.addWidget(self.y_2d_btn, 9, 2, 1, 1)

        right_layout.addLayout(right_layout2, 2, 0, alignement_top)

        self.setLayout(layout)

    def start_measure(self):
        tag.les_start(self.ser)
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.update_distance)
        self.timer.start()
        self.update_distance()
        self.measure_btn.setEnabled(0)
        self.stop_meas_btn.setEnabled(1)

    def start_measure_2d(self):
        tag.les_start(self.ser)
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.update_pos)
        self.timer.start()
        self.update_pos()
        self._2d_pos_btn_start.setEnabled(0)
        self._2d_pos_btn_stop.setEnabled(1)

    def stop_measure(self):
        tag.stop_shell_cmd(self.ser)
        self.timer.stop()
        self.measure_btn.setEnabled(1)
        self._2d_pos_btn_start.setEnabled(1)
        self.stop_meas_btn.setEnabled(0)

    def update_distance(self):
        dist = tag.les_read(self.ser)
        if dist:
            parts = dist.strip().split('=')
            val = parts[-1]
            self.distance_line.setText(val)

    def update_pos(self):
        pos = tag.les_read(self.ser)
        if pos:
            match = re.search(r"est\[(-?\d+\.\d+),(-?\d+\.\d+)", pos)
            if match:
                x, y = map(float, match.groups())
                self._2d_pos_line.setText(f"X = {x}, Y = {y}")
                self.x_pos, self.y_pos = x, y
                self.position_changed.emit(x, y)

    def set_2d_xy(self):
        x = self.x_2d_line.text()
        y = self.y_2d_line.text()

        tag.set_2d_xy(self.ser, x, y)

    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        self.terminal_textbox.clear()

        for port in ports:
            self.terminal_textbox.append(port.device)

    def set_mode(self):
        mode = self.mode_line.text()

        if mode == 'tag':
            tag.tag_moge(self.ser)
        elif mode == 'anchor':
            tag.an_mode(self.ser)
        else:
            QMessageBox.information(self, 'Cant recognize mode', 'set the mode correctly to tag or anchor')

        self.terminal_textbox.clear()
        self.terminal_textbox.append(tag.get_sys_info(self.ser))

    def set_update_rate(self):
        frequency = self.update_rate_line.text()
        valid = tag.update_rate(self.ser, frequency)
        print(valid)

        self.terminal_textbox.clear()
        self.terminal_textbox.append(tag.get_sys_info(self.ser))

    def set_panid(self):
        hex_panid = self.panid_line.text()
        tag.set_panid(self.ser, hex_panid)

        self.terminal_textbox.clear()
        self.terminal_textbox.append(tag.get_sys_info(self.ser))

    def set_node_label(self):
        node_label = self.node_label_line.text()
        tag.set_node_label(self.ser, node_label)

        self.terminal_textbox.clear()
        self.terminal_textbox.append(tag.anchors_list(self.ser))

    def show_anchors_list(self):
        self.terminal_textbox.clear()
        self.terminal_textbox.append(tag.anchors_list(self.ser))

    def serial_con_accept(self):
        port = self.serial_port_name_line.text()
        baudrate = int(self.baudrate_line.text())
        mode = self.mode_line.text()

        try:
            if not hasattr(self, 'ser') or self.ser is None or not self.ser.is_open:
                self.ser = tag.create_serial_connection(port, baudrate)
                QMessageBox.information(self, 'Success', f'port {port} has been opened')
            else:
                QMessageBox.information(self,'info', f'Connection with port {port} already exists')
            self.terminal_textbox.clear()
            self.terminal_textbox.append(tag.get_sys_info(self.ser))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'The port {port} cannot be opened, check your device meneger\n\n{e}')

        print(port, baudrate, mode)

    def reboot_module(self):
        tag.reboot(self.ser)
        self.terminal_textbox.clear()
        self.terminal_textbox.setText(tag.get_sys_info(self.ser))

    def show_module_mode(self):
        self.info_line.setStyleSheet('color: green;')
        self.info_line.setText('works')
        self.terminal_textbox.clear()
        self.terminal_textbox.setText(tag.get_mode(self.ser))