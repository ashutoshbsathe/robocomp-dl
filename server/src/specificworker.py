#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

from genericworker import *
from model import Net
import torch
import torch.nn.functional as F
import numpy as np
# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map):
        super(SpecificWorker, self).__init__(proxy_map)
        self.timer.timeout.connect(self.compute)
        self.Period = 2000
        self.timer.start(self.Period)
        self.model = Net()
        self.model.load_state_dict(torch.load('./ckpt/mnist_cnn.pt', map_location=torch.device('cpu')))
        self.model.eval()


    def __del__(self):
        print('SpecificWorker destructor')

    def setParams(self, params):
        #try:
        #	self.innermodel = InnerModel(params["InnerModelPath"])
        #except:
        #	traceback.print_exc()
        #	print("Error reading config params")
        return True

    @QtCore.Slot()
    def compute(self):
        print('SpecificWorker.compute...')
        #computeCODE
        #try:
        #	self.differentialrobot_proxy.setSpeedBase(100, 0)
        #except Ice.Exception as e:
        #	traceback.print_exc()
        #	print(e)

        # The API of python-innermodel is not exactly the same as the C++ version
        # self.innermodel.updateTransformValues('head_rot_tilt_pose', 0, 0, 0, 1.3, 0, 0)
        # z = librobocomp_qmat.QVec(3,0)
        # r = self.innermodel.transform('rgbd', z, 'laser')
        # r.printvector('d')
        # print(r[0], r[1], r[2])

        return True

# =============== Methods for Component Implements ==================
# ===================================================================

    #
    # processImage
    #
    def DLServer_processImage(self, img):
        #
        # implementCODE
        #
        image = torch.FloatTensor(np.fromstring(img.image,dtype=np.float32).reshape(-1, img.depth,img.width,img.height)) #1x28x28
        ret = F.softmax(self.model(image)).detach().numpy()
        return ret

# ===================================================================
# ===================================================================

