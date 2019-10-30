# Gym-game-emulated-control
Orange 600 PPR 2-Phase Incremental Optical Rotary Encoder was used. 

Implemented in python 3.6
Install gym & pynput  
Used Parallel processing to emulate keyboard/mouse.
For mouse emulation use Mouse Emulator file 

The Main File has three sections all runs parallely. 
1. Serial reads from arduino.
2. Emulates keyboard
3. Gym Game in Human Mode 

They communicate with each other by queue. 


