from compas_view2.collections import Collection
from compas_view2.shapes import Arrow

from .collectionobject import CollectionObject

import itertools
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Circle
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
        self.link_objs = {}
        self.create(robot.root, self)

    def create(self, link, parent, parent_joint=None):

        meshes = []

        for item in itertools.chain(link.visual):
            meshes.extend(Geometry._get_item_meshes(item))

        if meshes:
            obj = parent.add(Collection(meshes), name=link.name, show_edges=False)
        else:
            lines = []
            for joint in link.joints:
                line = Line([0, 0, 0], joint.origin.point)
                lines.append(line)
                if parent_joint:
                    lines.append(Circle(Plane([0, 0, 0], parent_joint.axis.vector), line.length/3))
            obj = parent.add(Collection(lines), name=link.name)

        if parent_joint:
            obj.matrix = Transformation.from_frame(parent_joint.origin).matrix
            self.joints[parent_joint.name] = {
                'link_obj': obj,
                'joint': parent_joint,
                'axis': parent_joint.axis.vector
            }

        self.link_objs[link.name] = obj

        for joint in link.joints:
            self.create(joint.child_link, parent=obj, parent_joint=joint)

    def rotate_joint(self, joint_name, angle):
        joint = self.joints[joint_name]
        T = Translation.from_vector(joint['link_obj'].translation)
        R = Rotation.from_axis_and_angle(joint['axis'], radians(angle))
        joint['link_obj'].matrix = (T * R).matrix
