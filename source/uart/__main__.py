'''
Uart driver for quickly testing the uart
'''

import argparse
import time
from source.uart.uart import Uart

def listen(uart):
    while True:
        uart.read_buffer()
        time.sleep(1)

def write(uart):
    while True:
        send = input("Send over UART: ")
        uart.send_string(send)
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', "--platform", default="laptop", help="Options: laptop, nano, pi")
    parser.add_argument('-m', "--mode", default="listen", help="Options: listen, send")
    args = vars(parser.parse_args())

    uart = Uart(state={"platform": args["platform"]})

    if args["mode"] == "listen":
        listen(uart)
    else:
        write(uart)
