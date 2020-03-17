'''
Uart driver for sending data to embedded board and receiving corresponding echo
'''

from .uart import Uart

uart = Uart()

while True:
    if uart.string():
        uart.read_buffer()
