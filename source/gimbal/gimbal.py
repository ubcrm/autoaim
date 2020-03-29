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
	
	def truncate_angle(self, angle):
		if angle > 180:
			return 180
		elif angle < -180:
			return -180
		return angle

	# Processes screen coords and frame and converts them to a set of angles
	# returns delta angles
	def process(self, x, y, frame_dims):
		adjusted_x = (frame_dims[0] / 2) - x
		adjusted_y = (frame_dims[1] / 2) - y
		horiz_angle = (adjusted_x / (frame_dims[0] / 2)) * self.properties["horiz_fov"]
		vert_angle = (adjusted_y / (frame_dims[1] / 2)) * self.properties["vert_fov"]
		return self.truncate_angle(horiz_angle), self.truncate_angle(vert_angle)
