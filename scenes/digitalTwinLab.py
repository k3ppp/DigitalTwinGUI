from asset import *

from connections.mjpegStream import MJPEGStream

from scenes.scene import Scene
from scenes.models.genericModel import GenericModel
from scenes.models.kukaRobot import KukaRobotTwin
from scenes.utils.movingCamera import MovingCamera
from scenes.utils.builder import Builder

from ui.elements.uiButton import UiButton
from ui.elements.uiWrapper import UiWrapper
from ui.elements.ui3dScene import Ui3DScene
from ui.elements.uiStream import UiStream
from ui.elements.uiWrapper import UiWrapper
from ui.elements.uiText import UiText
from ui.elements.uiSlider import UiSlider
from ui.constraintManager import *
from ui.uiHelper import *

from utils.mathHelper import *
from utils.videoPlayer import *

import numpy as np
import time

class DigitalTwinLab(Scene):

    UI_PADDING = 10

    def __init__(self, window, name):
        super().__init__(window, name)
        self.camera = MovingCamera(self.window, [12, 3, 1.5, -90, 0, -50], 2)
    @timing
    def createUi(self):
        self.renderWindow = Ui3DScene(self.window, Constraints.ALIGN_PERCENTAGE_PADDING(0, 0, 1, 1, DigitalTwinLab.UI_PADDING))
        self.renderWindow.setBackgroundColor((0.2, 0.2, 0.2))
        self.modelRenderer = self.renderWindow.getRenderer()
        self.sceneWrapper.addChild(self.renderWindow)
        
        self.panelWrapper = UiWrapper(self.window, Constraints.ALIGN_PERCENTAGE_PADDING(0.7,0,0.3,1, DigitalTwinLab.UI_PADDING))
        self.sceneWrapper.addChild(self.panelWrapper)

        self.__createRoom()
        self.__addRobots()
        self.__addFurniture()
        return
    
    def __createRoom(self):
        roomColor = (0.9,0.9,0.9,1)
        plan = [
            #right
            [(0,0),(0,1.1),(0,2.4)],
            [(0,1.1),(0,1.26),(0,3.1)],
            [(0,1.26),(0,6.92),(0,0.885)],
            [(0,6.92),(0,7),(0,3.1)],
            [(0,1.1),(0,6.92),(2.4,3.1)],

            #front
            [(0,0),(0.47,0),(0,2.4)],
            [(0.47,0),(1.47,0),(0,0.885)],
            [(3.77,0),(5.77,0),(0,0.885)],
            [(5.77,0),(6.39,0),(0,2.4)],
            [(6.39,0),(8.39,0),(0,0.885)],
            [(10.69,0),(11.69,0),(0,0.885)],
            [(11.69,0),(12.34,0),(0,2.4)],
            [(12.34,0),(15.3,0),(0,0.885)],

            #left door
            [(15.3,0),(15.3,1),(0,2.4)],
            [(15.3,1),(15.3,2.75),(0,0.885)],
            [(15.3,2.75),(15.3,2.9),(0,3.1)],
            [(15.3,5),(15.3,7),(0,3.1)],
            [(15.3,1.1),(15.3,7),(2.4,3.1)],

            [(15.43, 2.9), (15.3, 2.9), (0, 2.4)],
            [(15.43, 5), (15.3, 5), (0, 2.4)],

            [(15.43, 1), (15.3, 1), (0.885, 2.4)],
            [(15.43, 2.75), (15.3, 2.75), (0.885, 2.4)],

            #back
            [(0,7),(15.3,7),(0,0.885)],

            [(14.1,7),(15.3,7),(0.885,2.4)],
            [(12.32,7),(13.26,7),(0.885,2.4)],

            [(0,7),(1.3,7),(0.885,2.4)],
            [(2.15,7),(4,7),(0.885,2.4)],
            [(4.84,7),(5.94,7),(0.885,2.4)],

            [(6.31,7),(7.31,7),(0.885,2.4)],
            [(8.16,7),(9.9,7),(0.885,2.4)],
            [(10.75,7),(11.95,7),(0.885,2.4)],

            [(0,7),(15.3,7),(2.4,3.1)],
            
            #back pillars
            [(0,6.92),(0.3,6.92),(0,3.1)],
            [(0.3,6.92),(0.3,7),(0,3.1)],
            [(5.94,6.92),(6.31,6.92),(0,3.1)],
            [(5.94,6.92),(5.94,7),(0,3.1)],
            [(6.31,6.92),(6.31,7),(0,3.1)],
            [(11.95,6.92),(12.32,6.92),(0,3.1)],
            [(11.95,6.92),(11.95,7),(0,3.1)],
            [(12.32,6.92),(12.32,7),(0,3.1)],

            #side room
            [(15.3, 1),(17.96, 1),(0, 2.4)],
            [(17.96, 1),(17.96, 7),(0, 2.4)],
            [(15.43, 5),(15.43, 7),(0, 2.4)],
            [(15.3, 7),(17.96, 7),(0, 2.4)],
            [(15.43,1),(15.43,2.75),(0,0.885)],
            [(15.43,2.75),(15.43,2.9),(0,2.4)]]

        xyPlanes = [
            (0, 0, 2.4, 15.3, 1.1, Builder.S2),
            (0, 0, 0, 15.3, 7, Builder.S1|Builder.S2),
            (0, 1.1, 3.1, 15.3, 5.9, Builder.S2),
            (15.3, 1, 0, 0.13, 6, Builder.S1|Builder.S2),
            (15.3, 1, 0.885, 0.13, 1.75, Builder.S1),
            (15.3, 1, 2.4, 0.13, 6, Builder.S1|Builder.S2),
            (15.43, 1, 0, 2.53, 6, Builder.S1|Builder.S2),
            (15.43, 1, 2.4, 2.53, 6, Builder.S2)]
        
        self.roomPlan = Builder.buildWallPlan(plan)
        self.roomPlan.extend([Builder.buildPlaneXY(*plane[0:5], vis=plane[5]) for plane in xyPlanes])
        self.roomPlan.append(Builder.buildPlaneXZ(0, 1.1, 2.4, 15.3, 0.7, vis=Builder.S2))
        
        self.roomPlan = Model.fromSubModels(self.roomPlan)

        room = self.modelRenderer.addModel(self.roomPlan, np.identity(4))
        self.modelRenderer.setColor(room, roomColor)

        # for plane in Builder.buildWallPlan(plan):
        #     mid = self.modelRenderer.addModel(Builder.buildWallPlan(plan), np.identity(4))
        #     self.modelRenderer.setColor(mid, roomColor)
        
        # for plane in xyPlanes:
        #     mid = self.modelRenderer.addModel(Builder.buildPlaneXY(*plane[0:5], vis=plane[5]), np.identity(4))
        #     self.modelRenderer.setColor(mid, roomColor)

        # mid = self.modelRenderer.addModel(Builder.buildPlaneXZ(0, 1.1, 2.4, 15.3, 0.7, vis=Builder.S2), np.identity(4))
        # self.modelRenderer.setColor(mid, roomColor)
        return

    def __addRobots(self):
        self.bases = []
        self.arms = {}

        base = GenericModel(self.window, self.modelRenderer, Assets.KUKA_FLEX, createTransformationMatrix(6.3, 4.5, 0.89, 0, 0, 0))
        arm = KukaRobotTwin(self.window, createTransformationMatrix(0.315, 0, 0, 0, 0, 0), 23, 'R3', self.modelRenderer, hasForceVector=True, hasGripper=True)
        arm.setLiveColors([(1, 51/255, 51/255, 0.95)for i in range(9)])
        arm.setTwinColors([(1, 178/255, 102/255, 0.0)for i in range(9)])
        self.bases.append(base)
        self.arms[base] = arm

        # self.hamster = GenericModel(self.window, self.modelRenderer, Assets.SCREENSQ, np.matmul(createTransformationMatrix(0,0,-0.5,90,0,90), createScaleMatrix(0.2,0.2,0.2)))
        # self.hamsterPlayer = VideoPlayer.fromCapture(Assets.HAMSTER, fps=30)
        # self.modelRenderer.setTexture(self.hamster.modelId, self.hamsterPlayer.texture)
        # self.modelRenderer.setColor(self.hamster.modelId, (1,1,1,1))

        base = GenericModel(self.window, self.modelRenderer, Assets.KUKA_FLEX, createTransformationMatrix(6, 6, 0.89, 0, 0, -90))
        arm = KukaRobotTwin(self.window, createTransformationMatrix(0.315, 0, 0, 0, 0, 0), 24, 'R4', self.modelRenderer, hasForceVector=True, hasGripper=False)
        arm.setLiveColors([(1, 1, 0, 0.7)for i in range(9)])
        arm.setTwinColors([(1, 1, 153/255, 0.0)for i in range(9)])
        self.bases.append(base)
        self.arms[base] = arm
        
        base = GenericModel(self.window, self.modelRenderer, Assets.OMNIMOVE, createTransformationMatrix(11.3, 2.3, 0.7, 0, 0, 90))
        arm = KukaRobotTwin(self.window, createTransformationMatrix(0.363, -0.184, 0, 0, 0, -90), 21, 'R1', self.modelRenderer, hasForceVector=True, hasGripper=True)
        arm.setLiveColors([(0, 1, 0, 0.7)for i in range(9)])
        arm.setTwinColors([(102/255, 1, 178/255, 0.0)for i in range(9)])
        self.bases.append(base)
        self.arms[base] = arm
        
        base = GenericModel(self.window, self.modelRenderer, Assets.OMNIMOVE, createTransformationMatrix(13.4, 1.5, 0.7, 0, 0, 0))
        arm = KukaRobotTwin(self.window, createTransformationMatrix(0.363, -0.184, 0, 0, 0, -90), 22, 'R2', self.modelRenderer, hasForceVector=True, hasGripper=True)
        arm.setLiveColors([(0, 0.5, 1.0, 0.7)for i in range(9)])
        arm.setTwinColors([(153/255, 153/255, 1, 0.0)for i in range(9)])
        self.bases.append(base)
        self.arms[base] = arm

        [self.modelRenderer.setColor(model.modelId, (0.9,1.0,1.0,1.0)) for model in self.bases]

    def __addFurniture(self): 
        self.shelves = []
        self.shelves.append(self.modelRenderer.addModel(Assets.SHELF, createTransformationMatrix(14.70,2.4,0,0,0,-90)))
        self.shelves.append(self.modelRenderer.addModel(Assets.SHELF, createTransformationMatrix(12.1,0,0,0,0,0)))
        self.shelves.append(self.modelRenderer.addModel(Assets.SHELF, createTransformationMatrix(6.6,6.0,0,0,0,0)))
        self.shelves.append(self.modelRenderer.addModel(Assets.SHELF, createTransformationMatrix(16.75,4,0,0,0,-90)))

        self.tables = []
        self.tables.append(self.modelRenderer.addModel(Assets.TABLE_RECT, createTransformationMatrix(2.8,7-0.5,0.85,0,0,90)))
        self.tables.append(self.modelRenderer.addModel(Assets.TABLE_SQUARE, createTransformationMatrix(4.8,7-0.9,0.85,0,0,0)))
        # self.tables.append(self.modelRenderer.addModel(Assets.TABLE_RECT, createTransformationMatrix(9,7-0.5,0.85,0,0,90)))
        self.tables.append(self.modelRenderer.addModel(Assets.TABLE_RECT, createTransformationMatrix(10.1,6.5,0.85,0,0,90))) 
        self.tables.append(self.modelRenderer.addModel(Assets.TABLE_RECT, createTransformationMatrix(0.6,3.1,0.85,0,0,0)))
        self.tables.append(self.modelRenderer.addModel(Assets.TABLE_RECT, createTransformationMatrix(0.6,5.1,0.85,0,0,0)))
        # self.tables.append(self.modelRenderer.addModel(Assets.TABLE_RECT, createTransformationMatrix(7,0.8,0.85,0,0,90)))
        
        # self.Printer = []
        # self.Printer.append(self.modelRenderer.addModel(Assets.PrusaXL, createTransformationMatrix(0.6,3.3,0.85,0,0,0)))

        self.screenStreams = []
        self.screenStreams.append(MJPEGStream('http://172.32.1.226:8080/?action=streams'))
        # self.screenStreams.append(MJPEGStream('http://172.32.1.225:8080/?action=streams'))
        # self.screenStreams.append(MJPEGStream('http://172.32.1.226:8080/?action=streams'))
        # self.screenStreams.append(MJPEGStream('http://172.32.1.227:8080/?action=streams'))
        # self.screenStreams.append(MJPEGStream('http://172.32.1.228:8080/?action=streams'))
        self.screen = []
        self.screen.append(self.modelRenderer.addModel(Assets.SCREEN, createTransformationMatrix(8.8,6.99,1,90,0,90)))
        self.modelRenderer.setTexture(self.screen[0], self.screenStreams[0].texture)
        # self.screen.append(self.modelRenderer.addModel(Assets.SCREEN, createTransformationMatrix(11.8,6.99,1,90,0,90)))
        # self.modelRenderer.setTexture(self.screen[1], self.screenStreams[4].texture)
        # self.screen.append(self.modelRenderer.addModel(Assets.SCREEN, createTransformationMatrix(8.8,6.99,1,90,0,90)))
        # self.modelRenderer.setTexture(self.screen[2], self.screenStreams[3].texture)
        # self.screen.append(self.modelRenderer.addModel(Assets.SCREEN, createTransformationMatrix(0.01,6.1,0.885,90,90,90)))
        # self.modelRenderer.setTexture(self.screen[3], self.screenStreams[2].texture)
        # self.screen.append(self.modelRenderer.addModel(Assets.SCREEN, createTransformationMatrix(12,6.99,1,90,0,90)))
        # self.modelRenderer.setTexture(self.screen[1], self.screenStreams[1].texture)

    def handleUiEvents(self, event):
        [arm.handleEvents(event) for arm in self.arms.values()]
        [model.handleEvents(event) for model in self.bases]
        if event['action'] == 'release':
            if event['obj'] == self.renderWindow:
                self.__handleSceneEvents(event)
        return
    
    def __handleSceneEvents(self, event):
        modelId = event['modelId']
        self.panelWrapper.removeAllChildren()
        for arm in self.arms.values():
            if arm.isModel(modelId):
                self.renderWindow.updateWidth(COMPOUND(RELATIVE(T_W, 0.7, P_W), ABSOLUTE(T_W, -2*DigitalTwinLab.UI_PADDING)))
                self.panelWrapper.addChild(arm.getControlPanel())
        for model in self.bases:
            if model.isModel(modelId):
                self.renderWindow.updateWidth(COMPOUND(RELATIVE(T_W, 0.7, P_W), ABSOLUTE(T_W, -2*DigitalTwinLab.UI_PADDING)))
                self.panelWrapper.addChild(model.getControlPanel())
        if len(self.panelWrapper.children) == 0:
            self.renderWindow.updateWidth(COMPOUND(RELATIVE(T_W, 1, P_W), ABSOLUTE(T_W, -2*DigitalTwinLab.UI_PADDING)))
    
    def update(self, delta):
        # self.hamsterPlayer.update(delta) 

        self.__updateEnv(delta)
        self.__updateModelPos()
        [stream.updateImage(delta) for stream in self.screenStreams]
        [arm.update() for arm in self.arms.values()]
        [model.update(delta) for model in self.bases]
        return
    
    def __updateModelPos(self):
        for base in self.arms:
            self.arms[base].setAttach(base.getFrame())

        # self.hamster.setAttach(self.bases[0].getFrame())
        
        return
    
    def __updateEnv(self, delta):
        if self.window.selectedUi == self.renderWindow:
            self.camera.moveCamera(delta)
        if self.camera.hasMoved():
            self.modelRenderer.setViewMatrix(createViewMatrix(*self.camera.getCameraTransform()))
        
    def start(self):
        [arm.start() for arm in self.arms.values()]
        [stream.start() for stream in self.screenStreams]
        return
        
    def stop(self):
        [arm.stop() for arm in self.arms.values()]
        [stream.stop() for stream in self.screenStreams]
        return





