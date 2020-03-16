import serial
import time

ser = serial.Serial("/dev/ttyS0", 115200)

def read_buffer():
	received_data = ser.read()
	time.sleep(0.03)
	data_left = ser.inWaiting()
	received_data += ser.read(data_left)
	print(received_data)
	return received_data

def send_terminal(data_out=None):
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

def send_angle():
	print("hey")

if __name__ == "__main__":

	while True:
		data_sent_flag = send_terminal()
		#time.sleep(0.5)
		if data_sent_flag:
			read_buffer()
