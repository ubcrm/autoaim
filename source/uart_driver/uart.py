import serial
import time

ser = serial.Serial("/dev/ttyS0", 115200)

def listen():
	received_data = ser.read()
	time.sleep(0.03)
	data_left = ser.inWaiting()
	received_data += ser.read(data_left)
	print(received_data)

def send():
	data = input("Type: ")
	if data != "":
		ser.write(data.encode())
		return True
	else:
		print("Data must not be null")
		return False
		
if __name__ == "__main__":

	while True:
		data_sent_flag = send()
		#time.sleep(0.5)
		if data_sent_flag:
			listen()
