import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Define a size for the shapes
size = 1.0

# Calculate sizes so that the circumscribed radius ≈ size
cube_size = 2 * size / np.sqrt(3)
tetra_size = 4 * size / np.sqrt(6)
octa_size = size * np.sqrt(2)

# Create cube
cube = trimesh.creation.box(extents=[cube_size, cube_size, cube_size])
cube.apply_translation([0, 0, 0])

# Create regular tetrahedron

tetra_vertices = np.array([
    [0, 0, 0],
    [tetra_size, 0, 0],
    [tetra_size/2, tetra_size*np.sqrt(3)/2, 0],
    [tetra_size/2, tetra_size*np.sqrt(3)/6, tetra_size*np.sqrt(6)/3]
])
tetra = trimesh.convex.convex_hull(tetra_vertices)
tetra.apply_translation(-tetra.center_mass)

# Create regular octahedron
octa_vertices = np.array([
    [octa_size/2, 0, 0],
    [-octa_size/2, 0, 0],
    [0, octa_size/2, 0],
    [0, -octa_size/2, 0],
    [0, 0, octa_size/2],
    [0, 0, -octa_size/2]
])
octa = trimesh.convex.convex_hull(octa_vertices)
octa.apply_translation(-octa.center_mass)

# (Optional) You can keep the gen_combined_mesh function if needed for other uses.


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