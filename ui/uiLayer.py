from ui.elements.uiWrapper import UiWrapper
from ui.uiBatch import UiBatch

class UiLayer:

    MAX_BATCH_SIZE = 64

    def __init__(self, window):
        self.window = window
        
        self.masterElem = UiWrapper(self.window, [], (0, 0, *window.dim))

        self.hasMasterListChanged = False
        self.masterList = []

        self.batches = []
    
    def update(self, delta):
        if self.window.resized:
            self.__updateMasterElem()
        if self.masterElem.isDirtyComponents:
            self.__updateMasterList()
        if self.hasMasterListChanged:
            self.__updateRenderers()
        for elem in self.masterList:
            elem.update(delta)

    def render(self):
        for batch in self.batches:
            batch.render()

    def __updateRenderers(self):
        self.batches = []
        currentBatch = None
        for elem in self.masterList:
            for renderer in elem.getRenderers():
                if currentBatch != None and currentBatch.hasRoom(renderer):
                    currentBatch.addRenderer(renderer)
                    continue
                currentBatch = UiBatch(UiLayer.MAX_BATCH_SIZE)
                self.batches.append(currentBatch)
                currentBatch.addRenderer(renderer)
        self.hasMasterListChanged = False

    def __updateMasterList(self):
        self.masterList = []
        queue = [self.masterElem]
        while len(queue) > 0:
            elem = queue.pop(0)
            self.masterList.append(elem)
            queue.extend(elem.children)
        self.masterElem.setCleanComponents()
        self.hasMasterListChanged = True

    def __updateMasterElem(self):
        self.masterElem.dim = (0,0,*self.window.dim)
        self.masterElem.constraintManager.pos = (0,0)
        self.masterElem.constraintManager.dim = self.window.dim
        self.masterElem.setDirtyVertices()

    def getMasterElem(self):
        return self.masterElem
    

