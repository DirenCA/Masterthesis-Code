import numpy as np
import matplotlib.pyplot as plt

# Load Binary data
with open("/Users/direnakkaya/Downloads/DepthMap4.bin", "rb") as f:
    metadata = np.fromfile(f, dtype=np.float32, count=2)  #  width & height
    width, height = int(metadata[0]), int(metadata[1])
    depth_data = np.fromfile(f, dtype=np.float16)

# Checking Values
print(f"Width x Height: {width} x {height}")
print("Check first vlaues:", depth_data[:10])

#Depthmap to 2D
depth_map = depth_data.reshape((height, width))

# Checking plot
plt.figure(figsize=(10, 6))
plt.imshow(depth_map, cmap="plasma", interpolation="nearest")
plt.colorbar(label="Tiefe (Meter)")
plt.title(f"Tiefenkarte {width}x{height}")
plt.show()
