#This .py is for testing new functions, libaries, etc.

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ------Visualizing DepthMap and getting values for the depth------
url = r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\Tiefenkarten\20241207_171339_DepthMap.tiff"

im = Image.open(url) #Quelle: https://stackoverflow.com/a/67346474
#width, height = im.size

depth_array = np.array(im)


plt.imshow(depth_array)
plt.colorbar(label="Depth Value")
plt.title("DepthMap")
plt.ylabel("Height")
plt.xlabel("Width")
plt.show()

# Wertebereiche anzeigen (Min/Max)
depth_min = np.min(depth_array)
depth_max = np.max(depth_array)

print(depth_min, depth_max)
print(depth_array) #ggf. herausfinden, in welcher einheit sind (cm,mm,etc.)?

# ------Extracting DepthData in raw binary form------
