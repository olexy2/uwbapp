import serial
import time

def create_serial_connection(port, baudrate):
    return serial.Serial(port, baudrate, timeout=1)

def stop_shell_cmd(ser):
    stop = b'\r'
    ser.write(stop)
    data = ser.readline(50)
    time.sleep(0.5)

    print("Received bytes:", data)
    print("Received HEX:", data.hex())
    print("Decoded:", data.decode())

def access_uart(ser):
    enter = b'\r'
    time.sleep(1)
    ser.write(enter)
    time.sleep(0.1)
    ser.write(enter)
    time.sleep(1)
    print('uart accessed')

def an_mode(ser):
    ser.write(b'nma\r')

def tag_moge(ser):
    ser.write(b'nmt\r')

def set_panid(ser, panid):
    panid_str = str(panid).strip()
    ser.write(b'nis ')
    time.sleep(0.3)
    ser.write(panid_str.encode('utf-8') + b'\r')

def update_rate(ser, rate):
    rate_str = str(rate).strip()
    ser.write(b'aurs ')
    time.sleep(0.3)
    ser.write(rate_str.encode('utf-8') + b' ')
    time.sleep(0.3)
    ser.write(rate_str.encode('utf-8') + b'\r')

def set_node_label(ser, name):
    name_str = str(name).strip()
    ser.write(b'nls ')
    time.sleep(0.3)
    ser.write(name_str.encode('utf-8') + b'\r')

def anchors_list(ser):
    access_uart(ser)
    ser.write(b'la\r')
    time.sleep(0.5)

    response = ser.read_all().decode(errors='ignore')
    print(response)

    lines = response.strip().splitlines()[-6:]
    return '\n'.join(lines)

def reboot(ser):
    ser.write(b'reset\n')

def get_mode(ser):
    ser.write(b'nmg\r')
    time.sleep(0.2)
    data = ser.readline(50)
    time.sleep(0.1)
    return data

def les_start(ser):
    ser.write(b'les\r')

def les_read(ser):
    time.sleep(0.05)
    response = ser.read_all().decode(errors='ignore')
    return response

def set_2d_xy(ser, x, y):
    x_str = str(x).strip()
    y_str = str(y).strip()
    ser.write(b'aps ')
    time.sleep(0.1)
    ser.write(x_str.encode('utf-8')+b' ')
    time.sleep(0.1)
    ser.write(y_str.encode('utf-8')+b' ')
    time.sleep(0.1)
    ser.write(b'0\r')

def get_sys_info(ser):
    access_uart(ser)
    ser.write(b'si\r')
    time.sleep(0.5)

    response = ser.read_all().decode(errors='ignore')
    print(response)

    lines = response.strip().splitlines()[-10:]

    return "\n".join(lines)