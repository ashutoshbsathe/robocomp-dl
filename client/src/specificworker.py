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
import torch 
import torchvision.datasets as datasets 
import torchvision.transforms as transforms
import numpy as np
from timeit import default_timer as timer
# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel
DATASET_PATH = '/home/ashutosh/mnist_data'
class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map):
        super(SpecificWorker, self).__init__(proxy_map)
        self.timer.timeout.connect(self.compute)
        self.Period = 2000
        self.timer.start(self.Period)
        self.mnist_test_loader = iter(torch.utils.data.DataLoader(
                       datasets.MNIST(DATASET_PATH, train=False, transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ]), download=True), batch_size=1, shuffle=True))


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
        new_img, label = next(self.mnist_test_loader)
        img = TImage()
        img.width = 28
        img.height = 28
        img.depth = 1
        img.image = new_img.numpy().tobytes()
        start = timer()
        probs = self.dlserver_proxy.processImage(img)
        end = timer()
        prob_string = '[ ' + ' '.join('{:.3f}'.format(prob) for prob in probs) + ' ]'
        print(64*'-')
        print('Label: {}'.format(label.item()))
        print('Returned Probabilities: \n{}'.format(prob_string))
        print('Inferred Label: {}'.format(np.argmax(probs)))
        print('Elapsed Time: {:.4f}s'.format(end - start))
        print(64*'-')

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

