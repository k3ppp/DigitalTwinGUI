#!/usr/bin/env python3
import nest_asyncio

from window import *
from scenes.KukaScene import *
from scenes.EnvScene import *
from asset import *

nest_asyncio.apply()

window = Window((1200, 800), 'Digital Twin GUI Keenan Home', fullscreen=False, resizeable=True, vsync=False)

scene4 = EnvScene(window, 'Digital Twin')
scene4.createUi()


scene5 = KukaScene(window, 'Digital Twin')
scene5.createUi()

window.scenes.append(scene4)
window.scenes.append(scene5)


window.createUi()
window.run()
