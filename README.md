# Gym-game-emulated-control
**Hardware used**: 
• Orange 600 PPR 2-Phase Incremental Optical Rotary Encoder was used. 
• Arduino Uno 

**Software Requirement**: 
Implemented in python 3.6
Install gym & pynput  

**Architecture**:
For mouse emulation use Mouse Emulator file 

The MainFile.py has three sections all runs parallely using python Multiprocessing. 
1. Serial reads from arduino.
2. Emulates keyboard
3. Plays Gym Game in Human Mode 

They communicate with each other by queue. 


PWM_keyEmulator.py: If the encoder angle is greater than a particular threshold band it emulated couple of keys corresponding to the gym game control.

The mouseInterface.py: The mouse position is emulated to avatar position. 
