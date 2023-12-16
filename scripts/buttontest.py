from include.rcc_library import Raft
myraft = Raft()
myraft.setup_button()
while True:
    print(myraft.button())