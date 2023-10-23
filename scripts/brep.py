from compas_occ.brep import BRep
from compas.geometry import Box
from compas.geometry import Frame
from compas_view2.app import App

box = Box(Frame.worldXY(), 1, 1, 1)
brep = BRep.from_box(box)

viewer = App()
viewer.add(brep)
viewer.run()