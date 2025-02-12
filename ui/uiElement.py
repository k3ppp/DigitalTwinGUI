from constraintManager import *

from abc import abstractmethod
import OpenGL.GL as GL

class GlElement:
    def __init__(self, window, constraints, dim=(0,0,0,0)):
        self.window = window
        self.constraints = constraints
        self.dim = dim
        self.openGLDim = self.dim

        self.children = []
        self.parent = None
        self.isDirty = True
        self.constraintManager = ConstraintManager((self.dim[0], self.dim[1]), (self.dim[2], self.dim[3]))
        self.lastMouseState = self.window.mouseButtons

        self.zIndex = 0

        self.type = 'nothing'

    def update(self, delta):
        if self.isDirty and self.parent != None:
            relDim = self.parent.constraintManager.calcConstraints(*self.constraints)
            self.dim = (relDim[0] + self.parent.dim[0], relDim[1] + self.parent.dim[1], relDim[2], relDim[3])
            self.openGLDim = (
                (2*self.dim[0])/self.window.dim[0] - 1,
                (2*(self.window.dim[1]-self.dim[1]-self.dim[3]))/self.window.dim[1] - 1,
                (2*self.dim[2])/self.window.dim[0],
                (2*self.dim[3])/self.window.dim[1],
            )
            self.constraintManager.pos = (self.dim[0], self.dim[1])
            self.constraintManager.dim = (self.dim[2], self.dim[3])
            self.reshape()
            self.isDirty = False
        for child in self.children:
            child.update(delta)
        self.__actions()
        self.absUpdate(delta)
        return
    @abstractmethod
    def reshape(self):
        ...
    @abstractmethod
    def absUpdate(self, delta):
        ...
    
    def render(self):
        self.absRender()
        for child in self.children:
            child.render()
    @abstractmethod
    def absRender(self):
        ...
    
    def __actions(self):
        mousePos = self.window.mousePos
        self.isDefault = False
        if mousePos[0] > self.dim[0] and mousePos[0] < self.dim[0] + self.dim[2] and mousePos[1] > self.dim[1] and mousePos[1] < self.dim[1] + self.dim[3]:
            self.isDefault = False
            if self.window.mouseButtons[0] and not self.lastMouseState[0]:
                self.onPress()
                self.window.uiSelectBuffer.append(self)
            elif not self.window.mouseButtons[0] and self.lastMouseState[0]:
                self.onRelease()
            elif not self.window.mouseButtons[0] and not self.lastMouseState[0]:
                self.onHover()
            else:
                self.onHeld()
        elif not self.isDefault:
            self.onDefault()
            self.isDefault = True
        self.lastMouseState = self.window.mouseButtons

    def onDefault(self, callback=None):
        return
    
    def onHover(self, callback=None):
        return
    
    def onPress(self, callback=None):
        return
    
    def onRelease(self, callback=None):
        return
    
    def onHeld(self, callback=None):
        return

    def addChild(self, child):
        if child.parent != None: return
        if child in self.children: return
        child.setDirty()
        self.children.append(child)
        child.parent = self
    
    def addChildren(self, *children):
        for child in children:
            self.addChild(child)
    
    def removeChild(self, child):
        if child.parent != self: return
        if not child in self.children: return
        child.setDirty()
        self.children.remove(child)
        child.parent = None
    
    def removeChildren(self, *children):
        for child in children:
            self.removeChild(child)
    
    def removeAllChildren(self):
        for child in self.children:
            self.removeChild(child)
    
    def setDirty(self):
        self.isDirty = True
        for child in self.children:
            child.setDirty()

    def updateXPos(self, constraint):
        cIndex = -1
        if constraint.toChange != T_X: return
        for i,x in enumerate(self.constraints):
            if x.toChange != T_X: continue
            cIndex = i
            break
        self.constraints[cIndex] = constraint
        self.setDirty()

    def updateYPos(self, constraint):
        cIndex = -1
        if constraint.toChange != T_Y: return
        for i,x in enumerate(self.constraints):
            if x.toChange != T_Y: continue
            cIndex = i
            break
        self.constraints[cIndex] = constraint
        self.setDirty()

    def updateWidth(self, constraint):
        cIndex = -1
        if constraint.toChange != T_W: return
        for i,x in enumerate(self.constraints):
            if x.toChange != T_W: continue
            cIndex = i
            break
        self.constraints[cIndex] = constraint
        self.setDirty()

    def updateHeight(self, constraint):
        cIndex = -1
        if constraint.toChange != T_H: return
        for i,x in enumerate(self.constraints):
            if x.toChange != T_H: continue
            cIndex = i
            break
        self.constraints[cIndex] = constraint
        self.setDirty()


