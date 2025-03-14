import numpy as np
from pathlib import Path
import open3d as o3d
import matplotlib.pyplot as plt

def transform_binary_to_depthmap(binar_url):
    # Load Binary data
    input_path = Path(binar_url)
    with open(input_path, "rb") as f:
        metadata = np.fromfile(f, dtype=np.float32, count=2)  # width & height
        width, height = int(metadata[0]), int(metadata[1])
        depth_data = np.fromfile(f, dtype=np.float16)

    depth_map = depth_data.reshape((height, width))

    return depth_map

def extrude_pcd(pcd, visualize=True):
    pcd_object_array = np.asarray(pcd.points, dtype=np.float16)

    max_z_object = max(pcd_object_array[:, 2].tolist())
    new_points = []
    # Punkte in Z-Richtung erweitern

    for x, y, z in pcd_object_array:
        # Falls der Punkt zu tief liegt, Korrektur berechnen

        current_z = z
        while current_z < max_z_object:
            current_z += 0.0015
            if current_z > max_z_object:
                break
            new_points.append([x, y, current_z])

    # Neue Punkte zur Open3D Punktwolke hinzufügen
    new_points = np.array(new_points)  # Am Ende in ein numpy-Array umwandeln

    # Punktwolke der neuen Punkte visualisieren
    pcd_comp = o3d.geometry.PointCloud()
    pcd_comp.points = o3d.utility.Vector3dVector(new_points)

    if visualize:
        o3d.visualization.draw_geometries([pcd_comp], window_name="Ausgefülltes Objekt")

    return pcd_comp
