import compas
from compas.robots import GithubPackageMeshLoader
from compas.robots import RobotModel
from compas_view2.app import App
from compas_view2.collections import Collection

import itertools

from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.robots import Geometry
from math import radians, degrees

# github = GithubPackageMeshLoader('ros-industrial/abb', 'abb_irb6600_support', 'kinetic-devel')
# model = RobotModel.from_urdf_file(github.load_urdf('irb6640.urdf'))
# model.load_geometry(github)
model = RobotModel.ur5(True)

viewer = App(viewmode="lighted", enable_sceneform=True, enable_propertyform=True, enable_sidebar=True, width=2000, height=1000)

def create(link, parent=None, parent_joint=None):

    obj = None

    meshes = []

    for item in itertools.chain(link.visual):
        meshes.extend(Geometry._get_item_meshes(item))

    obj = parent.add(Collection(meshes), name=link.name, show_edges=False)

    if parent_joint:
        obj.matrix = Transformation.from_frame(parent_joint.origin).matrix

        @viewer.slider(title=parent_joint.name, minval=-180 , maxval=180)
        def rotate(angle):
            T = Translation.from_vector(obj.translation)
            R = Rotation.from_axis_and_angle(parent_joint.axis.vector, radians(angle))
            obj.matrix = (T * R).matrix
            viewer.view.update()

    for joint in link.joints:
        create(joint.child_link, parent = obj, parent_joint=joint)

create(model.root, viewer)

viewer.show()