import numpy as np
import cv2
from util.coordinateshow import draw_axis_on_img
import open3d as o3d
from scipy.spatial.transform import Rotation
import copy

if __name__ == "__main__":

    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    T = np.identity(4)

    img = np.zeros((480, 640, 3), dtype=np.uint8)
    # cv2.imshow("hello", img)
    # cv2.waitKey(0)

    rot = Rotation.from_euler("XYZ", [0, 0, 30], degrees=True).as_matrix()
    rotation_ = copy.deepcopy(rot)
    ans = draw_axis_on_img(img, rotation_)
    print(rot)

    T[:3, :3] = rot
    mesh.transform(T)
    o3d.visualization.draw_geometries([mesh])

    cv2.imshow("result", ans)
    cv2.waitKey(0)

    # z = Rotation.from_quat([0, 0, 0, 1]).as_matrix()
    # # print(z)
    # print(rot)
