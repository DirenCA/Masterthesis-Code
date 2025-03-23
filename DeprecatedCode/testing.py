# This .py is for testing new functions, libaries, etc.

from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d

# from PIL import Image
# im = Image.open(r"C:\Users\Diren\Nextcloud\DepthData-D0A666D9-65B4-4E3C-A73A-30D0A8B714BE.tiff")
# #im.show()
#
# lidar_iphone = np.array(im)
#
#
# # plotting the depthmap
# plt.imshow(lidar_iphone)
# plt.colorbar(label="Depth Value")
# plt.title("DepthMapIPhone")
# plt.ylabel("Height")
# plt.xlabel("Width")
# plt.show()
#
#
#
#
# # Konvertiere die Bilddaten in ein NumPy-Array
# im_array = np.array(im)
#
# # Gib den Datentyp der Pixel aus
# print(f"Datentyp: {im_array.dtype}")
# print(f"Shape: {im_array.shape}")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # CSV-Datei einlesen
# df = pd.read_csv(r"C:\Users\Diren\Nextcloud\depth_data.csv", delimiter=",")
#
# # X, Y und Depth-Werte extrahieren
# x = df["X"].to_numpy()
# y = df["Y"].to_numpy()
# depth = df["Depth(meters)"].to_numpy()
#
# # Maximale Dimensionen bestimmen
# width = int(x.max() + 1)  # Maximaler X-Wert bestimmt die Breite
# height = int(y.max() + 1)  # Maximaler Y-Wert bestimmt die Höhe
#
# # Leeres 2D-Array erstellen
# depth_map = np.zeros((height, width), dtype=np.float32)
#
# # Depth-Werte in das Array eintragen
# depth_map[y.astype(int), x.astype(int)] = depth

import tifffile as tiff
import numpy as np
import cv2


# TIFF-Datei laden (keine Skalierung, reine Werte!)
depth_array = tiff.imread(r"C:\Users\Diren\Nextcloud\DepthMap Kopie.tiff")

depth_array = cv2.cvtColor(depth_array, cv2.COLOR_RGB2GRAY)


#depth_array = np.array(depth_array)
print(depth_array.shape)

# Datentyp und Wertebereich prüfen
print(f"Datentyp: {depth_array.dtype}")  # Sollte float16 oder float32 sein
print(f"Shape: {depth_array.shape}")  # Erwartete Bildgröße (Höhe, Breite)
print(f"Minimale Tiefe: {np.min(depth_array)} Meter")
print(f"Maximale Tiefe: {np.max(depth_array)} Meter")





# Tiefenkarte plotten
plt.imshow(depth_array, cmap="viridis")
plt.colorbar(label="Depth (meters)")
plt.title("Depth Map (iPhone)")
plt.xlabel("Width")
plt.ylabel("Height")
plt.show()

# #%% md
# ## Taking Screesnhot
# #%%
#
# front = [ 0.84909464079690322, 0.19966150133689184, 0.48905375558712999 ]
# lookat = [ -0.015761666117579787, -0.0085461063453733683, 0.39159838485760257 ]
# up = [ 0.3842929910885669, 0.40173381379605055, -0.83122129415281698 ]
#
# zoom = 0.53999999999999981
#
# o3d.visualization.draw_geometries([pcd_object], front=front, lookat=lookat, up=up, zoom=zoom)
# #%%
# pcd_object
# #%%
# pcd_object_comp