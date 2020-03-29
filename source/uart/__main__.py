'''
Uart driver for quickly testing the uart
'''

from source.uart.uart import Uart

uart = Uart()

while True:
    uart.send_string()
