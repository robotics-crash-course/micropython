from sensors.odom import Odom

myleftencoder = Odom()
myleftencoder.setup(21)

while True:
    print(myleftencoder.count)