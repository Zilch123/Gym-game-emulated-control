import serial
import gym 
import  multiprocessing
from gym.envs.atari.atari_env import AtariEnv
from multiprocessing import Process, Lock
#rom gym.utils.play import *
import time
from time import perf_counter_ns
from pynput.keyboard import Key, Controller
from gym.utils.play import play
from gym.utils.play import PlayPlot



def serial_read(qu):
	ser = serial.Serial("COM11", 9600)
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
				# print("Data", data)
				qu.put(data)
		

def keyboard_emulator(qu, lock): 
	Th_angle1=1000
	Th_angle2=1000
	TonMax=10*10**6     #10*10**6 ns = 10 ms 
	TT_PWM= 15*10**6   #15*10**6 ns = 15 ms
	k1= Th_angle1/TonMax
	k2= Th_angle2/TonMax
	Offset=(9*10**6) 
	keyboard = Controller()
	while True:
		while not qu.empty():
			data=qu.get()
			
			lock.acquire()
			print("Data", data, qu.get())
			
			if(data<0):
				D2on= (abs(data)/k2)+Offset
				keyboard.press(key.up)
				t2_onstart = perf_counter_ns() 
				while((perf_counter_ns()-t2_onstart)<D2on): 
					pass
				t2_onstart=0
				keyboard.release(key.up)
				t2_offstart = perf_counter_ns()
				while((perf_counter_ns()-t2_offstart)<TonMax-D2on): 
					pass
				t2_offstart=0
				
			if(data>0):
				D1on= (data/k1)+Offset
				keyboard.press(key.down)
				t1_onstart = perf_counter_ns() 
				while((perf_counter_ns()-t1_onstart)<D1on): 
					pass
				t1_onstart=0
				keyboard.release(key.downdd)
				t1_offstart = perf_counter_ns()
				while((perf_counter_ns()-t1_offstart)<TonMax-D1on): 
					pass
				t1_offstart=0
				
			# if(data==0):
				# TonMax_trial= (250*10**6) 
				# D3on= (100*10**6) 
				# keyboard.press('d')
				# t2_onstart = perf_counter_ns() 
				# while((perf_counter_ns()-t2_onstart)<D3on): 
					# pass
				# t2_onstart=0
				# keyboard.release('d')
				# t2_offstart = perf_counter_ns()
				# while((perf_counter_ns()-t2_offstart)<TonMax_trial-D3on): 
					# pass
				# t2_offstart=0
				# pass
			else:
				pass
			lock.release()
			
def game_HM(score):
	def callback(obs_t, obs_tp1, action, rew, done, info):
		#print(obs_t, obs_tp1, action, rew, done, info)
		#print(obs_t)ad
		score.put(rew)

	
	env = AtariEnv(game= 'pong',mode=0,difficulty=1, obs_type='image', frameskip=1, full_action_space=False)
	# env = gym.make("BreakoutDeterministic-v4") #Breakout-v0 #Pong-v4 #BreakoutDeterministic-v4
	play(env, fps=15, zoom=3,callback=callback)
	
	
if __name__== "__main__":	
	qu= multiprocessing.Queue()
	score= multiprocessing.Queue()
	lock = Lock()
	
	process_serial_read= multiprocessing.Process(target=serial_read, args=(qu,))
	process_keyboard_emulator= multiprocessing.Process(target=keyboard_emulator, args=(qu,lock))
	process_game_HM= multiprocessing.Process(target=game_HM, args=(score,))
	
	process_serial_read.start()
	process_keyboard_emulator.start()
	process_game_HM.start()
	
	process_serial_read.join()
	process_keyboard_emulator.join()
	process_game_HM.join()
	
			
			