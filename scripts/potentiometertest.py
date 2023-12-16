from include.rcc_library import Raft
myraft = Raft()
myraft.setup_pot()
while True:
    print(myraft.get_pot())