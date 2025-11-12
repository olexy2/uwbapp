from PyQt6.QtWidgets import QMessageBox
import serial.tools.list_ports
import uart_communication as uart
import re

class Buttons_func:
    def __init__(self, main_window):
        self.main = main_window

    def update_distance(self):
        dist = uart.les_read(self.main.ser)
        if dist:
            parts = dist.strip().split('=')
            val = parts[-1]
            self.main.distance_line.setText(val)

    def start_measure(self):
        uart.les_start(self.main.ser)
        self.main.timer.timeout.disconnect()
        self.main.timer.timeout.connect(self.update_distance)
        self.main.timer.start()
        self.update_distance()
        self.main.measure_btn.setEnabled(False)
        self.main.stop_meas_btn.setEnabled(True)

    def stop_measure(self):
        uart.stop_shell_cmd(self.main.ser)
        self.main.timer.stop()
        self.main.measure_btn.setEnabled(True)
        self.main._2d_pos_btn_start.setEnabled(True)
        self.main.stop_meas_btn.setEnabled(False)

    def update_pos_2d(self):
        pos = uart.les_read(self.main.ser)
        if pos:
            match = re.search(r'est\[(-?\d+\.\d+),(-?\d+\.\d+)', pos)
            if match:
                x, y = map(float, match.groups())
                self.main._2d_pos_line.setText(f"X = {x}, Y = {y}")
                self.main.x_pos, self.main.y_pos = x, y
                self.main.position_changed.emit(x, y)

    def start_measure_2d(self):
        uart.les_start(self.main.ser)
        self.main.timer.timeout.disconnect()
        self.main.timer.timeout.connect(self.update_pos_2d)
        self.main.timer.start()
        self.update_pos_2d()
        self.main._2d_pos_btn_start.setEnabled(False)
        self.main._2d_pos_btn_stop.setEnabled(True)

    def set_2d_xy(self):
        x = self.main.x_2d_line.text()
        y = self.main.y_2d_line.text()
        uart.set_2d_xy(self.main.ser, x, y)

    def update_pos_3d(self):
        pos = uart.les_read(self.main.ser)
        if pos:
            match = re.search(r'est\[(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+)', pos)
            if match:
                x,y,z= map(float, match.groups())
                self.main._3d_pos_line.setText(f'X = {x}, Y = {y}, Z = {z}')
                self.main.x_pos, self.main.y_pos, self.main.z_pos = x, y, z
                self.main.position_changed.emit(x,y,z)

    def start_measure_3d(self):
        uart.les_start(self.main.ser)
        self.main.timer.timeout.disconnect()
        self.main.timer.timeout.connect(self.update_pos_3d)
        self.main.timer.start()
        self.update_pos_3d()
        self.main._3d_pos_btn_start.setEnabled(False)
        self.main._3d_pos_btn_stop.setEnabled(True)

    def set_3d_xyz(self):
        x = self.main.x_3d_line.text()
        y = self.main.y_3d_line.text()
        z = self.main.z_3d_line.text()
        uart.set_3d_xyz(self.main.ser, x, y, z)

    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        self.main.terminal_textbox.clear()
        self.main.serial_port_name_line.clear()

        for port in ports:
            self.main.terminal_textbox.append(port.device)
            self.main.serial_port_name_line.addItem(port.device)

    def set_mode(self):
        mode = self.main.mode_line.currentText()

        if self.main.ser is None:
            QMessageBox.warning(self.main, 'Error', 'No port is opened')
            return

        self.main.info_line.clear()

        if mode == 'tag':
            uart.tag_moge(self.main.ser)
            self.main.info_line.append('Mode has been set to TAG')
        elif mode == 'anchor':
            uart.an_mode(self.main.ser)
            self.main.info_line.append('Mode has been set to ANCHOR')
        else:
            QMessageBox.information(self.main, 'Error', 'Set the mode correctly to tag or anchor')

        self.main.terminal_textbox.clear()
        self.main.terminal_textbox.append(uart.get_sys_info(self.main.ser))

    def set_update_rate(self):
        frequency = self.main.update_rate_line.currentText()

        if self.main.ser is None:
            QMessageBox.warning(self.main, 'Error', 'No port is opened')
            return

        uart.update_rate(self.main.ser, frequency)
        self.main.info_line.clear()
        self.main.info_line.append(f'Update rate set to {frequency} s')
        self.main.terminal_textbox.clear()
        self.main.terminal_textbox.append(uart.get_sys_info(self.main.ser))

    def set_panid(self):
        hex_panid = self.main.panid_line.text().strip()

        if self.main.ser is None:
            QMessageBox.warning(self.main, 'Error', 'No port is opened')
            return

        if not hex_panid.startswith('0x'):
            QMessageBox.warning(self.main, 'Error', 'Use correct format (example: 0x00000A)')
            return

        try:
            int(hex_panid, 16)
        except ValueError:
            QMessageBox.warning(self.main, 'Error', 'PAN ID has to be hex number (example: 0x00000A)')
            return

        try:
            uart.set_panid(self.main.ser, hex_panid)
            info = uart.get_sys_info(self.main.ser)

            self.main.info_line.clear()
            self.main.info_line.append(f'PAN ID has been set to {hex_panid}')
            self.main.terminal_textbox.clear()
            self.main.terminal_textbox.append(info)

        except Exception as e:
            QMessageBox.critical(self.main, 'Error', f'Something went wrong: {e}')

    def set_node_label(self):
        node_label = self.main.node_label_line.text()
        uart.set_node_label(self.main.ser, node_label)

        self.main.info_line.clear()
        self.main.info_line.append(f'Node label has been set to {node_label}')
        self.main.terminal_textbox.clear()
        self.main.terminal_textbox.append(uart.get_sys_info(self.main.ser))

    def show_anchors_list(self):
        if self.main.ser is None:
            QMessageBox.warning(self.main, 'Error', 'No port is opened')
            return

        self.main.terminal_textbox.clear()
        self.main.terminal_textbox.append(uart.anchors_list(self.main.ser))

    def serial_con_accept(self):
        port = self.main.serial_port_name_line.currentText().strip()
        baudrate = self.main.baudrate_line.currentText().strip()

        if not port or not baudrate:
            QMessageBox.warning(self.main, 'Error', 'Set your serial port and baudrate first')
            return

        try:
            int_baudrate = int(baudrate)
        except ValueError:
            QMessageBox.warning(self.main, 'Error', 'Invalid Baudrate')
            return

        try:
            self.main.ser = uart.create_serial_connection(port, int_baudrate)
            QMessageBox.information(self.main, 'Connected', f'Successfully connected to {port}')
            self.main.terminal_textbox.clear()
            self.main.terminal_textbox.append(uart.get_sys_info(self.main.ser))
            self.main.info_line.clear()
            self.main.info_line.append(f'Port {port} connected')
        except Exception as e:
            QMessageBox.critical(self.main, 'Connection Error', f'Failed to connect:\n{e}')

    def reboot_module(self):
        if self.main.ser is None:
            QMessageBox.warning(self.main, 'Error', 'No port is opened')
            return

        uart.reboot(self.main.ser)
        self.main.terminal_textbox.clear()
        self.main.terminal_textbox.append(uart.get_sys_info(self.main.ser))
        self.main.info_line.clear()
        self.main.info_line.append('Module has been rebooted')

    def show_module_mode(self):
        if self.main.ser is None:
            QMessageBox.warning(self.main, 'Error', 'No port is opened')
            return

        mode = uart.get_mode(self.main.ser)

        self.main.terminal_textbox.clear()
        self.main.terminal_textbox.append(mode)
        self.main.info_line.clear()

        if 'an' in mode:
            self.main.info_line.append('Mode has been set to ANCHOR')
        elif 'tn' in mode:
            self.main.info_line.append('Mode has been set to TAG')
