
import vrep
import signal
import sys
from time import sleep
from sim import Sim

running = True

def signal_handler(sig, frame):
    global running
    running = False

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    sim = Sim()
    sim.connect()

    prismatic = sim.get_obj_handle('Prismatic_joint')
    revolute = sim.get_obj_handle('Revolute_joint')
    sim.init_joint(prismatic)
    sim.init_joint(revolute)
    sleep(0.2)

    target = 0.5

    while running:
        print sim.get_joint_position(revolute)
        sleep(0.1)

    sim.disconnect()
