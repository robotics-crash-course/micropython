from util.drivecontrol import Controller

mycontroller = Controller()
mycontroller.start()

while True:
    mycontroller.raft.led_off()
    mycontroller.drive_forwards() 

    if mycontroller.left_odom.count >= 1000:
        mycontroller.raft.led_on()
        mycontroller.left_turn() 
        mycontroller.left_odom.reset_count()