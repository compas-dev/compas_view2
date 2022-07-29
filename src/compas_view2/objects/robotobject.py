from compas_view2.collections import Collection

from .collectionobject import CollectionObject

import itertools

from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.robots import Geometry
from math import radians

class RobotObject(CollectionObject):
    """Object for displaying COMPAS RobotModel."""

    def __init__(self, robot, **kwargs):
        super().__init__(Collection(), name=robot.name, **kwargs)
        self.robot = robot
        self.joints = {}
        self.create(robot.root, self)

    def create(self, link, parent, parent_joint=None):

        meshes = []

        for item in itertools.chain(link.visual):
            meshes.extend(Geometry._get_item_meshes(item))
        
        obj = parent.add(Collection(meshes), name=link.name, show_edges=False)

        if parent_joint:
            obj.matrix = Transformation.from_frame(parent_joint.origin).matrix
            self.joints[parent_joint.name] = {
                'linkObj': obj,
                'joint': parent_joint,
                'axis': parent_joint.axis.vector
            }

        for joint in link.joints:
            self.create(joint.child_link, parent = obj, parent_joint=joint)
    
    def rotate_joint(self, joint_name, angle):
        joint = self.joints[joint_name]
        T = Translation.from_vector(joint['linkObj'].translation)
        R = Rotation.from_axis_and_angle(joint['axis'], radians(angle))
        joint['linkObj'].matrix = (T * R).matrix