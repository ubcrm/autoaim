from source.module import Module
from pathlib import Path
import serial
import time
import os


class Uart(Module):
    def __init__(self, parent=None, state=None):
        self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(self.working_dir, parent=parent, state=state)
		self.ser = serial.Serial("/dev/ttyS0", 115200)

	def read_buffer(self):
		received_data = ser.read()
		time.sleep(0.03)
		data_left = ser.inWaiting()
		received_data += ser.read(data_left)
		print(received_data)
		return received_data

	def send_string(self, data_out=None):
		if data_out is None:
			data = input("Type: ")
		else:
			data = data_out
		if data != "":
			ser.write(data.encode())
			return True
		else:
			print("Data must not be null")
			return False

	'''
	Angle parameter is a floating point number with value between 0.000 and 512.999
	'''
	def send_angle(self, angle):
		decimal = 0.0
		integer = 0
		checksum = 19
		bit_field = []
		mask = 1

		decimal = angle - round(angle)
		if decimal < 0:
			decimal = 1-decimal

		integer = int(angle)		
		bit_field = []

		for i in range(0,24):
			if (i < 10): 
				bit_field[i] = decimal & mask
			if (i < 19):
				bit_field[i] = integer & mask
			else:
				bit_field[i] = checksum & mask
			mask = mask << 1

		bit_string = ""

		for bit in bit_field:
			bit_string += str(bit)

		packet1 = bit_string[:8]
		packet2 = bit_string[8:16]
		packet3 = bit_string[16:24]

		Uart.send(packet1)
		Uart.send(packet1)
		Uart.send(packet1)
