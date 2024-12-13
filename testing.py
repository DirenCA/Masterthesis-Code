# This .py is for testing new functions, libaries, etc.

from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d
from camera_intrinsic import mtx

# ------Variablen------
depth_image_url = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\Tiefenkarten\20241207_171339_DepthMap.tiff"
rgb_image_url = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\TestBilder\20241207_171339.jpg"

depth_im = Image.open(depth_image_url)  # Quelle: https://stackoverflow.com/a/67346474
dm_width, dm_height = depth_im.size  # width and height of depthmap image

depth_array = np.array(depth_im)  # getting the depthmap as a numpy array

# print(depth_min, depth_max)
# print(depth_array)  # ggf. herausfinden, in welcher einheit die Entfernung angegeben ist (cm, mm, etc. ?) -> vermutlich cm?

# ------Create Pointcloud from DepthMap------

# I should first create a RGBD image using our depthmap and the rgb image

#print(f"height:{dm_height}, width:{dm_width}")  # need to scale our RGB image to the size of our depthmap image

rgb_im = Image.open(rgb_image_url)
rgb_im = ImageOps.exif_transpose(
    rgb_im)  # the picture will be rotated when opening based on the EXIF metadata. transpose stops that.
size = (dm_width, dm_height)  # define new size
rgb_im = rgb_im.resize(size)  # fitting the rgb image size to the size of the depth image

rgb_array = np.array(rgb_im)  # getting the rgb image as a numpy array

# convert the arrays to open3d objects Quelle: https://stackoverflow.com/questions/63587617/how-to-create-a-rgbd-image-from-numpy-rgb-array-and-depth-array
rgb_o3d = o3d.geometry.Image(rgb_array)
depth_o3d = o3d.geometry.Image(depth_array)

# Create an RGBD image Quelle: https://amanjaglan.medium.com/generating-3d-images-and-point-clouds-with-python-open3d-and-glpn-for-depth-estimation-a0a484d77570
# scale =  1.0
# depth_image = o3d.geometry.Image((depth_array / scale).astype(np.float32))    # brauchen wir eigentlich nicht
# rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
#     color=o3d.geometry.Image(np.zeros((dm_height, dm_width, 3), dtype=np.uint8)),
#     depth=depth_image,
#     convert_rgb_to_intensity=False
# )
#
# # Create the point cloud from the RGBD image
# pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
#     rgbd_image,
#     intrinsic # it seems that I need the camera intrinsic
# )    return pcd



# Create RGBD image

intrinsic = o3d.camera.PinholeCameraIntrinsic(dm_width, dm_height,
                                              mtx[0][0],  # fx
                                              mtx[1][1],  # fy
                                              mtx[0][2],  # cx
                                              mtx[1][2])  # cy

rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(rgb_o3d, depth_o3d)  # Quelle:https://www.open3d.org/docs/latest/python_api/open3d.geometry.RGBDImage.html und https://stackoverflow.com/questions/63587617/how-to-create-a-rgbd-image-from-numpy-rgb-array-and-depth-array

point_cloud = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, intrinsic)

o3d.visualization.draw_geometries([point_cloud])

# Visualisiere das Farbbild und Tiefenbild
# plt.subplot(1, 2, 1)
# plt.title("RGB Image")
# plt.imshow(rgb_o3d)
# plt.subplot(1, 2, 2)
# plt.title("Depth Image")
# plt.imshow(depth_o3d, cmap='gray')
# plt.show()

# plt.subplot(1, 2, 1)
# plt.title("Farbbild")
# plt.imshow(rgbd.color)
# plt.subplot(1, 2, 2)
# plt.title("Tiefenbild")
# plt.imshow(rgbd.depth)
# plt.show()pip  uns

# pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
#     rgbd,
#     o3d.camera.PinholeCameraIntrinsic(
#         o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
# # Flip it, otherwise the pointcloud will be upside down
# pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
# o3d.visualization.draw_geometries([pcd])