from ui.uiButton import UiButton
from ui.ui3dScene import Ui3DScene
from ui.uiWrapper import UiWrapper
from ui.uiStream import UiStream
from ui.uiVideo import UiVideo
from ui.uiWrapper import UiWrapper
from ui.uiTextInput import UiTextInput
from ui.uiText import UiText
from ui.uiSlider import UiSlider
from ui.uiImage import UiImage
from ui.mjpegStream import MJPEGStream

from utils.uiHelper import *
from utils.mathHelper import *
from connections.opcua import *

from constraintManager import *
from scenes.scene import *

from asyncua import ua
import pygame
from math import *

class KukaScene(Scene):
    
    def __init__(self, window, name):
        super().__init__(window, name)
        self.cameraTransform = [-0.7+5, -0.57+2, 1.5, -70.25, 0, 45]
        self.camSpeed = 2

        self.matchLive = True
        self.threadStopFlag = True

        return

    def createUi(self):
        padding = 10
        constraints = [
            ABSOLUTE(T_X, padding),
            ABSOLUTE(T_Y, padding),
            COMPOUND(RELATIVE(T_W, 1, P_W), ABSOLUTE(T_W, -2*padding)),
            COMPOUND(RELATIVE(T_H, 1, P_H), ABSOLUTE(T_H, -2*padding)),
        ]
        self.renderWindow = Ui3DScene(self.window, constraints)
        self.renderWindow.setBackgroundColor((1, 1, 1))
        self.modelRenderer = self.renderWindow.getRenderer()
        self.sceneWrapper.addChild(self.renderWindow)

        padding = 10
        constraints = [
            COMPOUND(COMPOUND(RELATIVE(T_X, 1, P_W), RELATIVE(T_X, -1, T_W)), ABSOLUTE(T_X, -padding)),
            ABSOLUTE(T_Y, padding),
            ABSOLUTE(T_W, 30),
            RELATIVE(T_H, 1, T_W)
        ]
        
        #RE TEXT Button example
        self.recenterBtn, self.recenterText = centeredTextButton(self.window, constraints)
        self.recenterText.setText('RE')
        self.recenterText.setFontSize(20)
        self.recenterText.setTextSpacing(7)
        self.recenterText.setTextColor((1, 1, 1))
        self.recenterBtn.setDefaultColor((0, 0, 0))
        self.recenterBtn.setHoverColor((0.1, 0.1, 0.1))
        self.recenterBtn.setPressColor((1, 0, 0))
        self.renderWindow.addChild(self.recenterBtn)
        constraints = [
            COMPOUND(RELATIVE(T_X, 0.7, P_W), ABSOLUTE(T_X, padding)),
            ABSOLUTE(T_Y, padding),
            COMPOUND(RELATIVE(T_W, 0.3, P_W), ABSOLUTE(T_W, -2*padding)),
            COMPOUND(RELATIVE(T_H, 0.8, P_H), ABSOLUTE(T_H, -2*padding)),
        ]

        self.panelWrapper = UiWrapper(self.window, constraints)
        self.sceneWrapper.addChild(self.panelWrapper)
                
        self.__createRoom()
        self.__addFurniture()

        return

    
    def __createRoom(self):
        roomDim = (7, 15.5)
        roomHeight = 2.7
        self.floor = self.modelRenderer.addModel(Assets.UNIT_WALL, createScaleMatrix(roomDim[0], roomDim[1], 1))
        self.walls = [0]*4
        self.walls[0] = self.modelRenderer.addModel(Assets.UNIT_WALL, 
            createTransformationMatrix(0, 0, roomHeight, 0, 90, 0).dot(createScaleMatrix(roomHeight, roomDim[1], 1)))
        self.walls[1] = self.modelRenderer.addModel(Assets.UNIT_WALL, 
            createTransformationMatrix(roomDim[0], 0, 0, 0, -90, 0).dot(createScaleMatrix(roomHeight, roomDim[1], 1)))
        self.walls[2] = self.modelRenderer.addModel(Assets.UNIT_WALL, 
            createTransformationMatrix(0, roomDim[1], 0, 90, 0, 0).dot(createScaleMatrix(roomDim[0], roomHeight, 1)))
        self.walls[3] = self.modelRenderer.addModel(Assets.UNIT_WALL, 
            createTransformationMatrix(0, 0, roomHeight, -90, 0, 0).dot(createScaleMatrix(roomDim[0], roomHeight, 1)))

    def __addFurniture(self):
        self.benches = [0]*5
        self.benches[0] = self.modelRenderer.addModel(Assets.TABLES[1], createTransformationMatrix(7-0.4, 0.8+1.05, 0.85, 0, 0, 0))
        self.benches[1] = self.modelRenderer.addModel(Assets.TABLES[1], createTransformationMatrix(7-1.05, 0.4, 0.85, 0, 0, 90))
        self.benches[2] = self.modelRenderer.addModel(Assets.TABLES[2], createTransformationMatrix(7-0.9, 0.8+2.1+0.9, 0.85, 0, 0, 0))
        self.benches[3] = self.modelRenderer.addModel(Assets.KUKA_BASE, createTransformationMatrix(7-0.9-0.7, 0.8+2.1+0.9-1.6, 0.85+0.06625, 0, 0, 0))
        self.benches[3] = self.modelRenderer.addModel(Assets.KUKA_BASE, createTransformationMatrix(7-1, 0.8+2.1+1.8+0.6, 0.85+0.06625, 0, 0, 0))

        x, y, z = 7-0.9-0.7+0.2, 0.8+2.1+0.9-1.6, 0.85+0.06625

        self.tubeIds = [0]*2
        self.tubeIds[0] = self.modelRenderer.addModel(Assets.TUBE_OUTSIDE, createTransformationMatrix(-0.134+x,0.805+y,0.0225+z,0,0,0))
        self.modelRenderer.setColor(self.tubeIds[0], (1, 1, 0, 1))
        self.tubeIds[1] = self.modelRenderer.addModel(Assets.TUBE_INSIDE, createTransformationMatrix(-0.134+x,0.805+y,0.0225+z,0,0,0))
        self.modelRenderer.setColor(self.tubeIds[1], (0.6, 0.6, 0.6, 1))
        
        self.tubeholderIds = [0]*4
        self.tubeholderIds[0] = self.modelRenderer.addModel(Assets.TUBE_HOLDER, createTransformationMatrix(-0.114+x,0.735+y,-0.06625+z,0,0,90))
        self.modelRenderer.setColor(self.tubeholderIds[0], (0.3, 0.3, 0.3, 1))
        self.tubeholderIds[1] = self.modelRenderer.addModel(Assets.TUBE_HOLDER, createTransformationMatrix(-0.004+x,0.735+y,-0.06625+z,0,0,90))
        self.modelRenderer.setColor(self.tubeholderIds[1], (0.3, 0.3, 0.3, 1))
        self.tubeholderIds[2] = self.modelRenderer.addModel(Assets.TUBE_HOLDER, createTransformationMatrix(-0.114+x,0.875+y,-0.06625+z,0,0,-90))
        self.modelRenderer.setColor(self.tubeholderIds[2], (0.3, 0.3, 0.3, 1))
        self.tubeholderIds[3] = self.modelRenderer.addModel(Assets.TUBE_HOLDER, createTransformationMatrix(-0.004+x,0.875+y,-0.06625+z,0,0,-90))
        self.modelRenderer.setColor(self.tubeholderIds[3], (0.3, 0.3, 0.3, 1))

        self.screenId = self.modelRenderer.addModel(Assets.SCREEN, createTransformationMatrix(6.99, 0.8+2.1+0.9-1, 0.9, 0, -90, 0))
        self.modelRenderer.setColor(self.screenId, (1,1,1,1))

        self.shelves = [0]*3
        self.shelves[0] = self.modelRenderer.addModel(Assets.SHELF, createTransformationMatrix(7-2.5, 0.8+2.1+1.8+1.3, 0, 0, 0, 0))
        self.shelves[1] = self.modelRenderer.addModel(Assets.SHELF, createTransformationMatrix(7-2.1-2.5,0,0,0,0,0))
        self.shelves[2] = self.modelRenderer.addModel(Assets.SHELF, createTransformationMatrix(1.2,3.9,0,0,0,90))

    
    def handleUiEvents(self, event):
        if event['action'] == 'release':
            if event['obj'] == self.recenterBtn:
                self.cameraTransform = [-0.7+5, -0.57+2, 1.5, -70.25, 0, 45]
            if event['obj'] == self.renderWindow:
                self.__handleSceneEvents(event)
        return
    
    def __handleSceneEvents(self, event):
        modelId = event['modelId']
        padding = 10
        self.panelWrapper.removeAllChildren()
        #DASHBOARD CLICK OPEN EXAMPLES
        # if modelId in self.twinKukaIds or modelId in self.modelKukaIds or modelId == self.gripperId or modelId == self.TgripperId:
        #     self.renderWindow.updateWidth(COMPOUND(RELATIVE(T_W, 0.7, P_W), ABSOLUTE(T_W, -2*padding)))
        #     self.panelWrapper.addChild(self.armControlPanel)
        # elif modelId in self.printers:
        #     index = self.printers.index(modelId)
        #     self.renderWindow.updateWidth(COMPOUND(RELATIVE(T_W, 0.7, P_W), ABSOLUTE(T_W, -2*padding)))
        #     self.panelWrapper.addChild(self.printerControlPanels[index])
        # else:
        #     self.renderWindow.updateWidth(COMPOUND(RELATIVE(T_W, 1, P_W), ABSOLUTE(T_W, -2*padding)))


    def absUpdate(self, delta):
        self.__moveCamera(delta)
        self.modelRenderer.setViewMatrix(createViewMatrix(*self.cameraTransform))
        return

    def __moveCamera(self, delta):
        if self.window.selectedUi != self.renderWindow:
            return

        if self.window.getKeyState(pygame.K_j):
            self.cameraTransform[5] -= 90*delta
        if self.window.getKeyState(pygame.K_l):
            self.cameraTransform[5] += 90*delta
        if self.window.getKeyState(pygame.K_i):
            self.cameraTransform[3] += 90*delta
        if self.window.getKeyState(pygame.K_k):
            self.cameraTransform[3] -= 90*delta
        
        deltaPos = [0,0,0]
        if self.window.getKeyState(pygame.K_a): #left
            deltaPos[0] -= 1
        if self.window.getKeyState(pygame.K_d): #right
            deltaPos[0] += 1
        if self.window.getKeyState(pygame.K_w): #forward
            deltaPos[1] -= 1
        if self.window.getKeyState(pygame.K_s): #back
            deltaPos[1] += 1
        if self.window.getKeyState(pygame.K_LALT): #down
            deltaPos[2] -= 1
        if self.window.getKeyState(pygame.K_SPACE): #up
            deltaPos[2] += 1
        deltaPos = [x*delta*self.camSpeed for x in normalize(deltaPos)]
        radPitch = radians(self.cameraTransform[3])
        radYaw = radians(self.cameraTransform[5])

        yawX =  deltaPos[0]*cos(radYaw)#+deltaPos[2]*sin(radYaw)
        yawY =  -deltaPos[0]*sin(radYaw)#+deltaPos[2]*cos(radYaw)

        self.cameraTransform[0] += yawX-deltaPos[1]*sin(radYaw)#*sin(radPitch)
        self.cameraTransform[1] += yawY-deltaPos[1]*cos(radYaw)#*sin(radPitch)
        self.cameraTransform[2] += -deltaPos[2]*sin(radPitch)#+deltaPos[1]*cos(radPitch)

    def start(self):
        self.threadStopFlag = False
        return
    
    def stop(self):
        self.threadStopFlag = True
        return
