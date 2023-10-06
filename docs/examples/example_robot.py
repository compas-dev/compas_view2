from compas.robots import GithubPackageMeshLoader
from compas.robots import RobotModel
from compas_view2.app import App
from compas.geometry import Box
from compas.geometry import Frame

github = GithubPackageMeshLoader('ros-industrial/abb', 'abb_irb6600_support', 'kinetic-devel')
model = RobotModel.from_urdf_file(github.load_urdf('irb6640.urdf'))
model.load_geometry(github)
# model = RobotModel.ur5(False)

viewer = App(viewmode="lighted", enable_sceneform=True, enable_sidebar=True, width=2000, height=1000)

robotObj = viewer.add(model)

end_effector_link_obj = robotObj.link_objs[model.get_end_effector_link_name()]
end_effector_link_obj.add(Box(Frame([0, 0, 0.25], [1, 0, 0], [0, 1, 0]), 0.2, 0.2, 0.5), name="end_effector_dummy_box")

for joint_name in model.get_configurable_joint_names():

    @viewer.slider(title=joint_name, minval=-180 , maxval=180)
    def rotate(angle, joint_name=joint_name):
        robotObj.rotate_joint(joint_name, angle)
        viewer.view.update()

viewer.show()