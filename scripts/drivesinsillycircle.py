from util.drivecontrol import Controller

mycontroller = Controller()
mycontroller.start()
mycontroller.raft.led_on()

while True:
    mycontroller.drive_forwards() 

    if mycontroller.left_odom.count >= 200:
        mycontroller.desired_theta += 10
        mycontroller.left_odom.reset_count()