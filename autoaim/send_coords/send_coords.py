import send_coords_config as CONFIG
from serial import Serial


class SendCoords:
    def __init__(self):
        self.serial = Serial(port=CONFIG.PORT, baudrate=CONFIG.BAUDRATE)

    def run(self, coords):
        self.serial.write(coords.encode())
