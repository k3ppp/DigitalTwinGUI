from ui.ui3dScene import Ui3DScene
from asset import *
from scenes.scene import *

class Bob(Scene):

    def buildPlaneXY(self, modelRenderer, x: float, y: float, dx: float, dy: float) -> None:
        vertices_xy = ([
            [x, y, 0],   # Bottom left
            [x+dx, y, 0],    # Bottom right
            [x+dx, y+dy, 0],     # Top right
            [x, y+dy, 0]     # Top left
        ])        

        plane = modelRenderer.addModel(vertices_xy, createTransformationMatrix(0, 0, 0, 0, 0, 0))
        return plane
        
