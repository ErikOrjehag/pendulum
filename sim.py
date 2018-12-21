
import vrep
import numpy as np

class Sim:
    def __init__(self):
        self._id = None
        self._flag = False

    def connect(self):
        vrep.simxFinish(-1)
        self._id = vrep.simxStart('127.0.0.1', 19997, True, True, 1000, 5)
        print 'connected to vrep (id: %d)' % self._id

    def disconnect(self):
        vrep.simxFinish(self._id)

    def error_check(self, res):
        if res != vrep.simx_return_ok:
            print 'An error occured! -> %d' % res

    def get_all_objects(self):
        res, objs = vrep.simxGetObjects(self._id, vrep.sim_handle_all, vrep.simx_opmode_oneshot_wait)
        self.error_check(res)
        return objs

    def get_obj_handle(self, name):
        res, handle = vrep.simxGetObjectHandle(self._id, name, vrep.simx_opmode_oneshot_wait)
        self.error_check(res)
        return handle

    def init_joint(self, handle):
        vrep.simxGetJointPosition(self._id, handle, vrep.simx_opmode_oneshot)

    def get_joint_position(self, handle):
        res, pos = vrep.simxGetJointPosition(self._id, handle, vrep.simx_opmode_oneshot)
        self.error_check(res)
        return pos

    def set_joint_force(self, handle, force):
        velocity = np.sign(force) * 1000.0
        vrep.simxSetJointTargetVelocity(self._id, handle, velocity, vrep.simx_opmode_oneshot)
        vrep.simxSetJointForce(self._id, handle, abs(force), vrep.simx_opmode_oneshot)
