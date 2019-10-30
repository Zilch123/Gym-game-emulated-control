import serial
import gym 
import  multiprocessing
from multiprocessing import Process, Lock
#rom gym.utils.play import *
import time
from time import perf_counter_ns
from pynput.mouse import Button, Controller
from gym.utils.play import play
from gym.utils.play import PlayPlot

def serial_read():
	ser = serial.Serial("COM11", 9600)
	#Balance
	xx=682
	dx=245
	yy=550

	mouse_factor=5
	mouse = Controller()
	mouse.position = (xx, yy)
	
	while True:
		s1=int.from_bytes(ser.read(),"big")
		s2=int.from_bytes(ser.read(),"big")
		if(s1==255 & s2==255):
			d1=int.from_bytes(ser.read(),"big")
			d2=int.from_bytes(ser.read(),"big")
			data=int.from_bytes(bytes([d1,d2]), byteorder='big', signed=True)
			cksum=int.from_bytes(ser.read(),"big")
			cksum0=sum([s1,s2,d1,d2]) % 256
			if(cksum==cksum0):
				deltax = xx+(data/mouse_factor)
				if(xx+dx>deltax>xx-dx):
					mouse.position = (deltax, yy)

if __name__== "__main__":	

	process_serial_read= multiprocessing.Process(target=serial_read)
	
	process_serial_read.start()

	process_serial_read.join()

			
