from source.uart.uart import Uart
from source.module import Module
from pathlib import Path
import os
import math


class Gimbal(Module):
	def __init__(self, parent=None, state=None):
		self.working_dir = Path(os.path.dirname(os.path.abspath(__file__)))
		super().__init__(self.working_dir, parent=parent, state=state)
		self.uart = Uart()

	def validate_current_angle(self, bits):
		checksum = 0
		for i in range(19,24): #bits 20-24 are checksum (indicies 19-23)
			try:
				checksum += int(bits[i])
				if i < 23:
					checksum = checksum << 1
			except:
				print('bit index out of range')
		if checksum == 19:   #0b10011
			return True 
		else:
			print("checksum failed with " + str(checksum) + " bits counted")
			return False

	# Processes screen coords and frame and converts them to a set of angles
	def process(self, x, y, frame_dims):
		adjusted_x = (frame_dims[0] / 2) - x
		adjusted_y = (frame_dims[1] / 2) - y
		horiz_angle = math.radians((adjusted_x / (frame_dims[0] / 2)) * self.properties["horiz_fov"])
		vert_angle = math.radians((adjusted_y / (frame_dims[1] / 2)) * self.properties["vert_fov"])
		return horiz_angle, vert_angle

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

		self.uart.send_string(packet1)
		self.uart.send_string(packet2)
		self.uart.send_string(packet3)
