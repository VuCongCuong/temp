import trimesh
import numpy as np

def create_substracted_mesh():
    # Tạo lập phương
    a = 1
    cube = trimesh.creation.box(extents=[a, a, a])
    cube.apply_translation([2, 2, 2])

    # Tạo tứ diện đều
    b = 1.5
    tetra_vertices = np.array([
        [0, 0, 0],
        [b, 0, 0],
        [b/2, b*np.sqrt(3)/2, 0],
        [b/2, b*np.sqrt(3)/6, b*np.sqrt(6)/3]
    ])
    tetra = trimesh.convex.convex_hull(tetra_vertices)
    tetra.apply_translation([2, 2, 2] - tetra.center_mass)

    # Tạo bát diện đều
    c = 1.5
    octa_vertices = np.array([
        [c/2, 0, 0],
        [-c/2, 0, 0],
        [0, c/2, 0],
        [0, -c/2, 0],
        [0, 0, c/2],
        [0, 0, -c/2]
    ])
    octa = trimesh.convex.convex_hull(octa_vertices)
    octa.apply_translation([2, 2, 2] - octa.center_mass)

    # Thực hiện phép giao nhau (intersection) để giữ lại phần chung của cả 3 khối
    substracted = trimesh.boolean.intersection([cube, tetra, octa], engine='blender')

    return substracted

# Ví dụ sử dụng:
if __name__ == "__main__":
    mesh = create_substracted_mesh()
    trimesh.Scene(mesh).show()