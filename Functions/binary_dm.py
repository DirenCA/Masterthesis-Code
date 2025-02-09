import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


def transform_binary_to_depthmap(binar_url):
    # Load Binary data
    input_path = Path(binar_url)
    with open(input_path, "rb") as f:
        metadata = np.fromfile(f, dtype=np.float32, count=2)  # width & height
        width, height = int(metadata[0]), int(metadata[1])
        depth_data = np.fromfile(f, dtype=np.float16)

    # Checking Values
    # print(f"Width x Height: {width} x {height}")
    # print("Check first vlaues:", depth_data[:10])

    # Depthmap to 2D
    depth_map = depth_data.reshape((height, width))

    return depth_map
