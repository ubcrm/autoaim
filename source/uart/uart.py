from source.module import Module
from pathlib import Path
import serial
import time
import os


class Uart(Module):
	def __init__(self, parent=None, state=None):
		self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
		super().__init__(self.working_dir, parent=parent, state=state)
		self.ser = serial.Serial(
			port='/dev/serial0' ,\
			baudrate=115200,\
			parity=serial.PARITY_NONE,\
			stopbits=serial.STOPBITS_ONE,\
			bytesize=serial.EIGHTBITS,\
				timeout=0)

	def read_buffer(self):
		received_data = self.ser.read()
		time.sleep(0.03)
		data_left = self.ser.inWaiting()
		received_data += self.ser.read(data_left)
		print(received_data.decode())
		return received_data.decode()

	def read_hex(self):
		str_num = self.read_buffer()
		hex_num = '0x'+(str_num.rstrip("\n\r"))
		print(hex_num)
		return hex_num

	def send_string(self, data_out=None):
		if data_out is None:
			data = input("Type: ")
			if data == "":
				print("Data must not be null")
				return False
			else:
				self.ser.write(data.encode())
		else:
			self.ser.write(data_out.encode())
		return True

