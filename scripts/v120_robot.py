from compas.robots import GithubPackageMeshLoader
from compas.robots import RobotModel
from compas_view2.app import App

github = GithubPackageMeshLoader('ros-industrial/abb', 'abb_irb6600_support', 'kinetic-devel')
model = RobotModel.from_urdf_file(github.load_urdf('irb6640.urdf'))
model.load_geometry(github)
# model = RobotModel.ur5(True)

viewer = App(viewmode="lighted", enable_sceneform=True, enable_sidebar=True, width=2000, height=1000)

robotObj = viewer.add(model)

for joint_name in robotObj.joints:

    @viewer.slider(title=joint_name, minval=-180 , maxval=180)
    def rotate(angle, joint_name=joint_name):
        robotObj.rotate_joint(joint_name, angle)
        viewer.view.update()

viewer.show()