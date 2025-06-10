import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Tạo lập phương
a = 1
cube = trimesh.creation.box(extents=[a,a,a])
cube.apply_translation([2,2,2])

# Tạo tứ diện đều
b = 1.5
tetra_vertices = np.array([
    [0, 0, 0],
    [b, 0, 0],
    [b/2, b*np.sqrt(3)/2, 0],
    [b/2, b*np.sqrt(3)/6, b*np.sqrt(6)/3]
])
tetra = trimesh.convex.convex_hull(tetra_vertices)
tetra.apply_translation([2,2,2] - tetra.center_mass)

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
octa.apply_translation([2,2,2] - octa.center_mass)

print("Cube is volume:", cube.is_volume)
print("Tetra is volume:", tetra.is_volume)
print("Octa is volume:", octa.is_volume)

# Combine (union) 3 khối

# combined = trimesh.boolean.union([cube, tetra, octa], engine='blender')

# trimesh.Scene(combined).show()



# intersected = trimesh.boolean.intersection([cube, tetra, octa], engine='blender')

# trimesh.Scene(intersected).show()


intersected = trimesh.boolean.intersection([cube, tetra, octa], engine='blender')

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
def plot_trimesh(ax, mesh, color):
    for face in mesh.faces:
        tri = mesh.vertices[face]
        poly = Poly3DCollection([tri], alpha=0.5, facecolor=color, edgecolor='k')
        ax.add_collection3d(poly)

# Vẽ từng mesh (bạn có thể bật/tắt từng dòng để xem riêng từng khối)
# plot_trimesh(ax, cube, 'red')
# plot_trimesh(ax, tetra, 'green')
# plot_trimesh(ax, octa, 'blue')

# Vẽ phần giao nhau (intersection) với màu vàng nổi bật
plot_trimesh(ax, intersected, 'yellow')

# Thiết lập giới hạn trục
ax.set_xlim(0, 4)
ax.set_ylim(0, 4)
ax.set_zlim(0, 4)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('Cube, Tetrahedron, Octahedron and Intersection')
plt.tight_layout()
plt.show()