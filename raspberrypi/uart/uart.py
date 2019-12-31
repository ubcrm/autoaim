import serial
import time

ser = serial.Serial("/dev/ttyS0", 115200)

def listen():
	received_data = ser.read()
	time.sleep(0.03)
	data_left = ser.inWaiting()
	received_data += ser.read(data_left)
	print(received_data)
	#ser.write(received_data)

def send():
	data = input("Type: ")
	ser.write(data.encode())

while True:
	send()
	#time.sleep(0.5)
	listen()
