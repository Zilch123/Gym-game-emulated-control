import serial
import gym 
import multiprocessing
#rom gym.utils.play import *
import time
from time import perf_counter_ns 
from pynput.keyboard import Key, Controller
from gym.utils.play import play
from gym.utils.play import PlayPlot


keyboard = Controller()
ser = serial.Serial("COM11", 9600)
Th_angle1=150
Th_angle2=150
Th_t=50000
TonMax=10*10^6 #10*10^6 ns = 10 ms

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
			print("Data", data, "Threshold", Th_t)
			if(data>0):
				keyboard.press('d')
				t1on_start = perf_counter_ns() 
				while((perf_counter_ns()-t1on_start)<Th_t): 
					pass
			
			
			
			
			
			
			if(data>Th_angle1):
				keyboard.press('d')
				t1_start = perf_counter_ns() 
				while((perf_counter_ns()-t1_start)<Th_t): 
					pass
				keyboard.release('d')
			elif(data<-Th_angle2):
				keyboard.press('a')
				t2_start = perf_counter_ns() 
				while((perf_counter_ns()-t2_start)<Th_t): 
					pass
				keyboard.release('a')
			else:
				keyboard.release('a')
				keyboard.release('d')
			
			
			
			