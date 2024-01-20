#Jeannette 1/20

from include.rcc_library import Raft

myraft = Raft()
# myraft.led_on()

myraft.setup_button()

while(True):
    if(myraft.get_button()):
        myraft.led_on()
    else:
        myraft.led_off()