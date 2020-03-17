'''
Uart driver for sending data to embedded board and receiving corresponding echo
'''

from source.uart_driver.uart import Uart

uart = Uart()

while True:
    if uart.string():
        uart.read_buffer()
