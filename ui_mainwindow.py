from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QGridLayout, QWidget, QLineEdit, QPushButton,
    QLabel, QTextEdit, QComboBox
)
from main_functions import Buttons_func

class MainWindow(QWidget):

    position_changed = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()

        self.bf = Buttons_func(self)

        self.ser = None

        self.setWindowTitle('UWB APP')
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet('background-color: #24272B;')

        self.x_pos = 0
        self.y_pos = 0

        # -------------------- LABELS -----------------------

        self.config_label = QLabel('Configurate UWB Module')
        self.measurements_label = QLabel('Measurements')
        self._2d_pos_label = QLabel('2D positioning')
        self.x_2d_label = QLabel('set anchor X coordinate [mm]')
        self.y_2d_label = QLabel('set anchor Y coordinate [mm]')
        self._3d_pos_label = QLabel('3D positioning')
        self.x_3d_label =QLabel('set anchor X coordinate [mm]')
        self.y_3d_label = QLabel('set anchor Y coordinate [mm]')
        self.z_3d_label = QLabel('set anchor Z coordinate [mm]')
        self.serial_port_name_label = QLabel('Serial port name')
        self.baudrate_label = QLabel('Baudrate')
        self.mode_label = QLabel('Mode')
        self.panid_label = QLabel('Personal Area Network ID (hex)')
        self.update_rate_label = QLabel('Update Rate [Hz]')
        self.node_label = QLabel('Node Label')

        # -------------------- LINE EDITS/COMBO BOXES --------

        #COLUMN 0
        self.serial_port_name_line = QComboBox(self)
        self.baudrate_line = QComboBox(self)
        self.mode_line = QComboBox(self)
        self.panid_line = QLineEdit(self)
        self.update_rate_line = QComboBox(self)
        self.node_label_line = QLineEdit(self)
        self.info_line = QTextEdit()
        self.terminal_textbox = QTextEdit()


        #COLUMN 1
        self.distance_line = QLineEdit()
        self._2d_pos_line = QLineEdit()
        self.x_2d_line = QLineEdit()
        self.y_2d_line = QLineEdit()
        self._3d_pos_line = QLineEdit()
        self.x_3d_line = QLineEdit()
        self.y_3d_line = QLineEdit()
        self.z_3d_line = QLineEdit()

        self.distance_line.setReadOnly(True)
        self._2d_pos_line.setReadOnly(True)

        # -------------------- BUTTONS --------------------

        #COLUMN 0
        self.connect_btn = QPushButton('connect')
        self.save_changes_btn = QPushButton('accept')  # ACCEPT 1
        self.set_panid_btn = QPushButton('accept')  # ACCEPT 2
        self.update_rate_btn = QPushButton('accept')  # ACCEPT 3
        self.node_label_accept = QPushButton('accept')  # ACCEPT 4
        self.xy_2d_btn = QPushButton('accept X and Y')  # ACCEPT 5
        self.xyz_3d_btn = QPushButton('accept X, Y, Z') #ACCEPT 6
        self.get_serial_ports_btn = QPushButton('get serial ports')
        self.reboot_btn = QPushButton('reboot the module')
        self.anchors_list_btn = QPushButton('show anchors in network')
        self.module_mode_btn = QPushButton('show module mode')

        #COLUMN 1
        self.measure_btn = QPushButton('start distance measuring')
        self.stop_meas_btn = QPushButton('stop distance measuring')
        self._2d_pos_btn_start = QPushButton('start 2D positioning')
        self._2d_pos_btn_stop = QPushButton('stop 2D positioning')
        self._3d_pos_btn_start = QPushButton('start 3D positioning')
        self._3d_pos_btn_stop = QPushButton('stop 3D positioning')

        # -------------------- TIMER --------------------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.bf.update_distance)
        self.timer.setInterval(100)
        self.timer.stop()

        # -------------------- OTHER METHODS --------------------
        self.build_ui()
        self.apply_styles()
        self.connect_signals()

    def build_ui(self):
        layout = QGridLayout()
        layout.setVerticalSpacing(5)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        alignement_top = Qt.AlignmentFlag.AlignTop

        #---------------- LEFT LAYOUT ----------------
        main_left_layout = QGridLayout()

        main_left_layout.addWidget(self.config_label, 0, 0, alignement_top)
        main_left_layout.addWidget(self.terminal_textbox, 2, 0)

        left_layout_1 = QGridLayout()

        left_layout_1.addWidget(self.serial_port_name_label, 0, 0)
        left_layout_1.addWidget(self.baudrate_label, 1, 0)
        left_layout_1.addWidget(self.mode_label, 4, 0)
        left_layout_1.addWidget(self.panid_label, 5, 0)
        left_layout_1.addWidget(self.update_rate_label, 6, 0)
        left_layout_1.addWidget(self.node_label, 7, 0)

        left_layout_1.addWidget(self.connect_btn, 2, 0, 1, 3)
        left_layout_1.addWidget(self.save_changes_btn, 4, 2)
        left_layout_1.addWidget(self.set_panid_btn, 5, 2)
        left_layout_1.addWidget(self.update_rate_btn, 6, 2)
        left_layout_1.addWidget(self.node_label_accept, 7, 2)
        left_layout_1.addWidget(self.get_serial_ports_btn, 3, 0, 1, 3)
        left_layout_1.addWidget(self.reboot_btn, 8, 0)
        left_layout_1.addWidget(self.anchors_list_btn, 8, 1, 1, 2)
        left_layout_1.addWidget(self.module_mode_btn, 9, 0)

        left_layout_1.addWidget(self.serial_port_name_line, 0, 1, 1, 3)
        left_layout_1.addWidget(self.baudrate_line, 1, 1, 1, 3)
        left_layout_1.addWidget(self.mode_line, 4, 1)
        left_layout_1.addWidget(self.panid_line, 5, 1)
        left_layout_1.addWidget(self.update_rate_line, 6, 1)
        left_layout_1.addWidget(self.node_label_line, 7, 1)
        left_layout_1.addWidget(self.info_line, 10, 0, 1, 3)

        layout.addLayout(main_left_layout, 0, 0)
        main_left_layout.addLayout(left_layout_1, 1, 0)

        # ---------------- RIGHT LAYOUT ----------------
        right_layout = QGridLayout()

        right_layout1 = QGridLayout()
        right_layout1.setContentsMargins(0, 0, 0, 0)


        layout.addLayout(right_layout, 0, 1)
        right_layout.addLayout(right_layout1, 1, 0, alignement_top)

        right_layout2 = QGridLayout()
        #right_layout2.setContentsMargins(0, 0, 0, 0)


        right_layout2.addWidget(self.measurements_label, 0, 0, 1, 3)
        right_layout2.addWidget(self.distance_line, 1, 0, 1, 3)
        right_layout2.addWidget(self.measure_btn, 2, 0, 1, 3)
        right_layout2.addWidget(self.stop_meas_btn, 3, 0, 1, 3)

        right_layout2.addWidget(self._2d_pos_label, 4, 0, 1, 3)
        right_layout2.addWidget(self._2d_pos_line, 5, 0, 1, 3)
        right_layout2.addWidget(self._2d_pos_btn_start, 6, 0, 1, 3)
        right_layout2.addWidget(self._2d_pos_btn_stop, 7, 0, 1, 3)
        right_layout2.addWidget(self.x_2d_label, 8, 0, 1, 1)
        right_layout2.addWidget(self.y_2d_label, 9, 0, 1, 1)
        right_layout2.addWidget(self.x_2d_line, 8, 1, 1, 1)
        right_layout2.addWidget(self.y_2d_line, 9, 1, 1, 1)
        right_layout2.addWidget(self.xy_2d_btn, 9, 2, 1, 1)
        right_layout2.addWidget(self._3d_pos_label, 10, 0, 1, 3)
        right_layout2.addWidget(self._3d_pos_line, 11, 0, 1, 3)
        right_layout2.addWidget(self._3d_pos_btn_start, 12, 0, 1, 3)
        right_layout2.addWidget(self._3d_pos_btn_stop, 13, 0, 1, 3)
        right_layout2.addWidget(self.x_3d_label, 14, 0, 1, 1)
        right_layout2.addWidget(self.y_3d_label, 15, 0, 1, 1)
        right_layout2.addWidget(self.z_3d_label, 16, 0, 1, 1)
        right_layout2.addWidget(self.x_3d_line, 14, 1, 1, 1)
        right_layout2.addWidget(self.y_3d_line, 15, 1, 1, 1)
        right_layout2.addWidget(self.z_3d_line, 16, 1, 1, 1)
        right_layout2.addWidget(self.xyz_3d_btn, 16, 2, 1, 1)

        right_layout.addLayout(right_layout2, 2, 0, alignement_top)

        self.setLayout(layout)

    def apply_styles(self):

        # ---------------- PLACEHOLDERS/LIST ITEMS----------------

        #COLUMN 0
        self.serial_port_name_line.setPlaceholderText('(None)')
        self.baudrate_line.setPlaceholderText('(None)')
        self.baudrate_line.addItems(['9600', '19200', '38400', '57600', '115200', '230400'])
        self.mode_line.setPlaceholderText('(None)')
        self.mode_line.addItems(['anchor', 'tag'])
        self.panid_line.setPlaceholderText('(None)')
        self.update_rate_line.setPlaceholderText('(None)')
        self.update_rate_line.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.node_label_line.setPlaceholderText('(None)')

        #COLUMN 1
        self.distance_line.setPlaceholderText('distance [m]')
        self._2d_pos_line.setPlaceholderText('[X, Y]')
        self._3d_pos_line.setPlaceholderText('[X, Y, Z]')

        self.info_line.setEnabled(False)
        self.terminal_textbox.setEnabled(False)

        ## ---------------- FONTS ----------------
        big_font = QFont()
        small_font = QFont()
        tiny_font = QFont()

        big_font.setPointSize(32)
        small_font.setPointSize(12)
        tiny_font.setPointSize(10)

        self.config_label.setFont(big_font)
        self.measurements_label.setFont(big_font)
        self._2d_pos_label.setFont(big_font)
        self._3d_pos_label.setFont(big_font)

        self.config_label.setStyleSheet('color: blue')
        self.measurements_label.setStyleSheet('color: orange')
        self._2d_pos_label.setStyleSheet('color: magenta')
        self._3d_pos_label.setStyleSheet('color: green')

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
            self._3d_pos_line,
            self._3d_pos_btn_start,
            self._3d_pos_btn_stop,
            self.x_3d_line,
            self.y_3d_line,
            self.z_3d_line,
            self.x_3d_label,
            self.y_3d_label,
            self.z_3d_label,
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

        self.info_line.setStyleSheet('color: green')

        white_tiny_font_widgets = [
            self.save_changes_btn,
            self.set_panid_btn,
            self.update_rate_btn,
            self.node_label_accept,
            self.xy_2d_btn,
            self.xyz_3d_btn,
        ]

        for widget in white_tiny_font_widgets:
            if isinstance(widget, QPushButton):
                widget.setFont(tiny_font)
                widget.setStyleSheet('color: white; background-color: #3D3D40;')

    def connect_signals(self):

        self.connect_btn.clicked.connect(self.bf.serial_con_accept)
        self.save_changes_btn.clicked.connect(self.bf.set_mode)
        self.set_panid_btn.clicked.connect(self.bf.set_panid)
        self.update_rate_btn.clicked.connect(self.bf.set_update_rate)
        self.node_label_accept.clicked.connect(self.bf.set_node_label)
        self.xy_2d_btn.clicked.connect(self.bf.set_2d_xy)
        # Create xyz_3d_btn function
        self.get_serial_ports_btn.clicked.connect(self.bf.get_serial_ports)
        self.reboot_btn.clicked.connect(self.bf.reboot_module)
        self.anchors_list_btn.clicked.connect(self.bf.show_anchors_list)
        self.module_mode_btn.clicked.connect(self.bf.show_module_mode)

        self.measure_btn.clicked.connect(self.bf.start_measure)
        self.stop_meas_btn.clicked.connect(self.bf.stop_measure)
        self._2d_pos_btn_start.clicked.connect(self.bf.start_measure_2d)
        self._2d_pos_btn_stop.clicked.connect(self.bf.stop_measure)
