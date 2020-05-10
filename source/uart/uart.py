from source.module import Module
from pathlib import Path
import serial
import time
import os


class Uart(Module):
	def __init__(self, parent=None, state=None):
		self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
		super().__init__(self.working_dir, parent=parent, state=state)
		self.platform = state["platform"]

		if (self.platform == "laptop"):
			self.port = '/dev/ttyUSB0'
		else:
			self.port = '/dev/serial0'

		self.ser = serial.Serial(
			port=self.port ,\
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
		#print(received_data)
		return received_data.decode()


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
