# This .py is for testing new functions, libaries, etc.

from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d
from camera_intrinsic import mtx

# ------------------------Variablen------------------------
depth_image_url = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\IphoneTestBilder\testi2.jpg"
rgb_image_url = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\TestBilder\20241214_125237_staerke7.jpg"

depth_im = Image.open(depth_image_url)  # Quelle: https://stackoverflow.com/a/67346474
dm_width, dm_height = depth_im.size  # width and height of depthmap image. we need to resize the rgb image later to this size to combine depth map and RGB image and create a RGBD image.


#---Iphone---

uurl = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\IphoneTestBilder\testi2.jpg"
depth_im = Image.open(uurl)

depth_im = Image.open(depth_image_url)  # Quelle: https://stackoverflow.com/a/67346474
dm_width, dm_height = depth_im.size  # width and height of depthmap image

depth_array = np.array(depth_im)  # getting the depthmap as a numpy array

# plotting the depthmap
plt.imshow(depth_array)
plt.colorbar(label="Depth Value")
plt.title("DepthMap")
plt.ylabel("Height")
plt.xlabel("Width")
plt.show()

depth_o3d = o3d.geometry.Image(depth_array)

# Intrinsische Kameraparameter (angepasst an Ihre Kamera)
intrinsic = o3d.camera.PinholeCameraIntrinsic(
    width=depth_array.shape[1],  # Bildbreite
    height=depth_array.shape[0],  # Bildhöhe
    fx=500,  # Brennweite in x-Richtung
    fy=500,  # Brennweite in y-Richtung
    cx=depth_array.shape[1] / 2,  # Optische Achse in x-Richtung (Bildmitte)
    cy=depth_array.shape[0] / 2   # Optische Achse in y-Richtung (Bildmitte)
)


depth_data_uint16 = (depth_array.astype(np.uint16)) #Quelle: https://stackoverflow.com/questions/73067231/how-to-convert-uint8-image-to-uint16-python
depth_uint16_o3d = o3d.geometry.Image(depth_data_uint16)

# Erstelle eine Point Cloud aus dem Tiefenbild
pcd = o3d.geometry.PointCloud.create_from_depth_image(
    depth_uint16_o3d,
    intrinsic
)

o3d.visualization.draw_geometries([pcd])
