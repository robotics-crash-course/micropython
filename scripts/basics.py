# from machine import Pin

# outputpin = Pin(0, Pin.OUT)
# outputpin.value(1)

# inputpin = Pin(4, Pin.IN)

# while True:
#     print(inputpin.value())

from include.rcc_library import Raft

myraft = Raft()

myraft.setup_button()
myraft.setup_button_counter()

while True:
    print(myraft.get_button(), myraft.button_counter())