import open3d as o3d
import numpy as np

def compute_voxel_volume(pcd, voxel_size, visualize=True):
    # Voxelgrid aus der Punktwolke erstellen
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)

    # Berechne das Volumen (m³)
    voxel_volumen_m3 = len(voxel_grid.get_voxels()) * (voxel_size ** 3)

    # Volumenberechnung
    voxel_volumen_ml = voxel_volumen_m3 * 1_000_000 #Umrechnung in cm³
    print(f"Geschätztes Volumen der Punktwolke: {voxel_volumen_ml:.2f} ml")

    # Optional: Visualisierung
    if visualize:
        o3d.visualization.draw_geometries([voxel_grid], window_name="Voxel-Visualisierung")

    return voxel_volumen_ml

def compute_convex_hull_volume(pcd, visualize=True):

    # Konvexe Hülle berechnen
    hull_mesh, hull_vertices = pcd.compute_convex_hull()

    # Liniennetz aus dem Hüllmesh erzeugen
    hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull_mesh)
    hull_ls.paint_uniform_color([1, 0, 0])  # Rot einfärben

    # Volumen der konvexen Hülle berechnen
    volume = hull_mesh.get_volume()
    volume_cm = volume * 1_000_000  # Umrechnung in cm³

    print(f"Geschätztes Volumen der konvexen Hülle: {volume_cm:.2f} ml")

    # Optional: Visualisierung
    if visualize:
        o3d.visualization.draw_geometries([pcd, hull_ls], window_name="Konvexe Hülle")

    return volume_cm


def compute_oriented_bounding_box_volume(pcd, visualize=True):
    # Oriented Bounding Box (OBB) berechnen
    oriented_bb = pcd.get_minimal_oriented_bounding_box()
    oriented_bb.color = (0, 1, 0)  # Grün einfärben

    # Volumenberechnung der OBB
    obb_extents = oriented_bb.extent  # Breite, Höhe, Tiefe
    obb_volume_m3 = np.prod(obb_extents)  # Volumen in m³
    obb_volume_cm3 = obb_volume_m3 * 1_000_000  # Umrechnung in cm³

    print(f"Geschätztes Volumen der OBB: {obb_volume_cm3:.2f} cm³")

    # Optional: Visualisierung
    if visualize:
        o3d.visualization.draw_geometries([pcd, oriented_bb], window_name="Oriented Bounding Box")

    return obb_volume_cm3
#test

def compute_alpha_shape_volume(pcd, alpha, visualize=True):
    #Quelle: https://stackoverflow.com/questions/1406029/how-to-calculate-the-volume-of-a-3d-mesh-object-the-surface-of-which-is-made-up

    # Normalenberechnung
    nn_distance = np.mean(pcd.compute_nearest_neighbor_distance())
    radius_normals = nn_distance * 4

    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normals, max_nn=16),
                         fast_normal_computation=True)
    pcd.paint_uniform_color([0.6, 0.6, 0.6])  # Einheitliches Grau

    # 2. Alpha Shape Berechnung

    alpha_shape = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
    alpha_shape.compute_vertex_normals()

    # 3. Volumenberechnung mit Tetrahedral Decomposition
    def compute_mesh_volume(mesh):
        vertices = np.asarray(mesh.vertices)
        triangles = np.asarray(mesh.triangles)

        volume = 0.0
        for tri in triangles:
            v0, v1, v2 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]
            tetra_volume = np.dot(v0, np.cross(v1, v2)) / 6.0  # Volumen eines Tetraeders
            volume += tetra_volume

        return abs(volume)

    alpha_volume_cm3 = compute_mesh_volume(alpha_shape) * 1_000_000  # Umrechnung in cm³
    print(f"Volumen: {alpha_volume_cm3:.2f} cm³")

    # # Optional: Visualisierung
    if visualize:
        o3d.visualization.draw_geometries([alpha_shape], mesh_show_back_face=True, window_name="Alpha Shape")

    return alpha_volume_cm3
