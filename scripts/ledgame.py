from include.rcc_library import Raft

myraft = Raft()

age = 15
fruit = "banana"

if fruit == "banana" and age > 13:
    print("led is on")
    myraft.led_on()
else:
    print("not true")