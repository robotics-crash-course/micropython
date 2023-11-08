# from machine import ADC
import raft

myraft = Raft()

while True:
    print(myraft.read_pot(), myraft.read_button())