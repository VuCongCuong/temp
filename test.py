#!/usr/bin/env python3
"""
combine_cube_octahedron.py

Tạo mesh giao của lập phương và bát diện đều tại cùng tâm mà không sử dụng engine boolean ngoài và không cần rtree.
"""
import trimesh
import numpy as np


def point_in_mesh(point: np.ndarray, mesh: trimesh.Trimesh) -> bool:
    """
    Kiểm tra điểm nằm trong mesh bằng cách đếm số lần tia xuất phát từ điểm giao cắt mesh.
    Nếu số lần cắt là lẻ => trong mesh.
    """
    # Tia theo phương +X
    origins = point.reshape((1, 3))
    directions = np.array([[1.0, 0.0, 0.0]])
    locations, index_ray, index_tri = mesh.ray.intersects_location(origins, directions)
    return len(index_ray) % 2 == 1


def subtract_and_combine_cube_octahedron(size=1.0):
    """
    Tạo mesh giao (intersection) giữa lập phương và bát diện đều cùng tâm.
    - size: kích thước biến cho cả hai hình.
    Trả về:
      - inter_mesh: Trimesh object của khu vực giao.
    """
    # 1. Tạo lập phương
    cube = trimesh.creation.box(extents=[size, size, size])
    # 2. Tạo bát diện đều thủ công
    points = np.array([
        [ size,  0.0,  0.0],
        [-size,  0.0,  0.0],
        [ 0.0,  size,  0.0],
        [ 0.0, -size,  0.0],
        [ 0.0,  0.0,  size],
        [ 0.0,  0.0, -size]
    ])
    faces = np.array([
        [0, 2, 4], [2, 1, 4], [1, 3, 4], [3, 0, 4],
        [0, 5, 2], [2, 5, 1], [1, 5, 3], [3, 5, 0]
    ])
    octa = trimesh.Trimesh(vertices=points, faces=faces, process=True)

    # 3. Căn giữa cả hai mesh về gốc
    cube.apply_translation(-cube.centroid)
    octa.apply_translation(-octa.centroid)

    # 4. Lấy đỉnh thuộc vùng giao
    cube_inside = np.array([v for v in cube.vertices if point_in_mesh(v, octa)])
    octa_inside = np.array([v for v in octa.vertices if point_in_mesh(v, cube)])

    # 5. Lọc mặt giao: cả 3 đỉnh đều nằm trong vùng giao
    inter_cube_faces = []
    for face in cube.faces:
        pts = cube.vertices[face]
        if all(point_in_mesh(pt, octa) for pt in pts):
            inter_cube_faces.append(face)
    inter_octa_faces = []
    for face in octa.faces:
        pts = octa.vertices[face]
        if all(point_in_mesh(pt, cube) for pt in pts):
            inter_octa_faces.append(face)
    inter_cube_faces = np.array(inter_cube_faces)
    inter_octa_faces = np.array(inter_octa_faces)

    # 6. Ghép đỉnh và mặt
    if cube_inside.size == 0:
        cube_inside = np.empty((0, 3))
    if octa_inside.size == 0:
        octa_inside = np.empty((0, 3))
    inter_vertices = np.vstack([cube_inside, octa_inside])
    inter_faces = []
    # Tạo map chỉ số
    cube_map = {tuple(v): i for i, v in enumerate(cube_inside)}
    octa_map = {tuple(v): i + len(cube_inside) for i, v in enumerate(octa_inside)}

    for face in inter_cube_faces:
        try:
            inter_faces.append([cube_map[tuple(cube.vertices[i])] for i in face])
        except KeyError:
            pass
    for face in inter_octa_faces:
        try:
            inter_faces.append([octa_map[tuple(octa.vertices[i])] for i in face])
        except KeyError:
            pass

    # 7. Tạo mesh kết quả và làm sạch
    inter_mesh = trimesh.Trimesh(vertices=inter_vertices, faces=np.array(inter_faces), process=True)
    inter_mesh.remove_duplicate_faces()
    inter_mesh.remove_degenerate_faces()
    inter_mesh.remove_unreferenced_vertices()
    inter_mesh = inter_mesh.process(validate=True)

    return inter_mesh


if __name__ == '__main__':
    mesh = subtract_and_combine_cube_octahedron(size=1.0)
    print(f"Intersection mesh: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
    try:
        mesh.show()
    except Exception:
        print("Không thể hiển thị mesh. Hãy xuất file hoặc dùng PyVista để xem.")
