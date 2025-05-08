import vtk
from model.abaqus_part import Part
from PySide6.QtWidgets import QVBoxLayout, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("MiddleButtonPressEvent", self.middle_button_press_event)
        self.AddObserver("MiddleButtonReleaseEvent", self.middle_button_release_event)
        self.AddObserver("RightButtonPressEvent", self.right_button_press_event)
        self.AddObserver("RightButtonReleaseEvent", self.right_button_release_event)

    def middle_button_press_event(self, obj, event):
        self.StartPan()
        return

    def middle_button_release_event(self, obj, event):
        self.EndPan()
        return

    def right_button_press_event(self, obj, event):
        self.StartPan()
        return

    def right_button_release_event(self, obj, event):
        self.EndPan()
        return

    def OnLeftButtonDown(self):
        self.Rotate()

    def OnMiddleButtonDown(self):
        self.Pan()

class VTKMeshViewer(QWidget):
    def __init__(self, parent:QWidget):

        super().__init__(parent)

        self.grain_actors = []
        colors = vtk.vtkNamedColors()
        self.Rotating = 0
        self.Panning = 0
        self.Zooming = 0

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setMinimumSize(800, 600)  # Set the minimum dimensions for the widget

        # Create a VTK render window interactor
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        layout.addWidget(self.vtk_widget)

        self.setLayout(layout)
        # Set up the VTK renderer
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.vtk_widget.SetInteractorStyle(CustomInteractorStyle())
        # Initialize and start the interactor
        self.vtk_widget.Initialize()
        self.vtk_widget.Start()

        # Load and display the mesh
        self.renderer.SetBackground(colors.GetColor3d("LightBlue"))  # Light background
        # Render
        self.vtk_widget.GetRenderWindow().Render()

        # draw axes
        self.add_axes_actor()

        # default view port
        self.set_default_view()
        self.add_workspace_plane()

        self.renderer.GetActiveCamera().Dolly(0.8)
        self.renderer.ResetCameraClippingRange()


    def load_mesh(self, part: Part, base=True):
        
        # Create VTK points
        points = vtk.vtkPoints()
        points.SetNumberOfPoints(len(part.nodes)+1)
        for i, x, y, z in part.nodes:
            points.SetPoint(i, (x, y, z))
            
        # Create VTK cells
        cells = vtk.vtkCellArray()
        for element in part.elements:
            if len(element) == 4:
                cell = vtk.vtkTriangle()
            if len(element) == 5:
                cell = vtk.vtkTetra()
            if len(element) == 6:
                cell = vtk.vtkPyramid()
            else: 
                cell = vtk.vtkHexahedron()
            element = element[1: len(element)]
            for j, point_id in enumerate(element):
                cell.GetPointIds().SetId(j, point_id)  # VTK uses 0-based indexing
            cells.InsertNextCell(cell)

        # Create PolyData
        mesh = vtk.vtkUnstructuredGrid()
        mesh.SetPoints(points)
        mesh.SetCells(vtk.VTK_TETRA if len(part.elements[0]) == 4 else vtk.VTK_HEXAHEDRON, cells)

        # Create Mapper
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(mesh)

        # Create Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetEdgeColor(0.1, 0.1, 0.1)  # Set grid color
        actor.GetProperty().EdgeVisibilityOn()  # Show grid

        # Add actor to renderer
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

        if not base:
            self.grain_actors.append(actor)

    def remove_mesh(self):
        """Remove all actors from the renderer.
        """
        for actor in self.grain_actors:
            self.renderer.RemoveActor(actor)
        
        # Update the renderer to reflect the changes
        self.vtk_widget.GetRenderWindow().Render()
    def add_axes_actor(self):
        axes = vtk.vtkAxesActor()
        self.orientation_widget = vtk.vtkOrientationMarkerWidget()
        self.orientation_widget.SetOrientationMarker(axes)
        self.orientation_widget.SetInteractor(self.vtk_widget.GetRenderWindow().GetInteractor())
        # self.orientation_widget.SetViewport(0.0, 0.0, 0.2, 0.2)
        self.orientation_widget.SetEnabled(1)
        self.orientation_widget.InteractiveOn()

    def set_default_view(self, scale=200):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(scale, scale, 0.5 * scale)  # Position the camera at an offset in X, Y, and Z
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin (or a central point in your scene)
        camera.SetViewUp(0, 0, scale)  # Set the up direction to be the Y-axis

        self.renderer.ResetCamera()  # Adjust the view to fit the scene
        self.vtk_widget.GetRenderWindow().Render()  # Render the scene with the new camera view

    def set_front_view(self, scale=200):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(scale, 0, 0)  # Position the camera along the negative Z-axis
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin (or a point on the XY plane)
        camera.SetViewUp(0, 0, scale)  # Set the up direction to be the positive Y-axis
        self.renderer.ResetCamera()  # Adjust the view to fit the scene
        self.vtk_widget.GetRenderWindow().Render()  # Render the scene with the new camera view

    def set_back_view(self, scale=200):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(-scale, 0, 0)  # Position the camera along the negative Z-axis
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin (or a point on the XY plane)
        camera.SetViewUp(0, 0, scale)  # Set the up direction to be the positive Y-axis
        self.renderer.ResetCamera()  # Adjust the view to fit the scene
        self.vtk_widget.GetRenderWindow().Render()  # Render the scene with the new camera view

    def set_left_view(self, scale=200):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, -scale, 0)  # Position the camera along the negative Z-axis
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin (or a point on the XY plane)
        camera.SetViewUp(0, 0, scale)  # Set the up direction to be the positive Y-axis
        self.renderer.ResetCamera()  # Adjust the view to fit the scene
        self.vtk_widget.GetRenderWindow().Render()  # Render the scene with the new camera view

    def set_right_view(self, scale=200):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, scale, 0)  # Position the camera along the negative Z-axis
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin (or a point on the XY plane)
        camera.SetViewUp(0, 0, scale)  # Set the up direction to be the positive Y-axis
        self.renderer.ResetCamera()  # Adjust the view to fit the scene
        self.vtk_widget.GetRenderWindow().Render()  # Render the scene with the new camera view

    def set_bottom_view(self, scale=200):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, 0, -scale)  # Position the camera along the negative Z-axis
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin (or a point on the XY plane)
        camera.SetViewUp(0, scale, 0)  # Set the up direction to be the positive Y-axis
        self.renderer.ResetCamera()  # Adjust the view to fit the scene
        self.vtk_widget.GetRenderWindow().Render()  # Render the scene with the new camera view

    def set_top_view(self, scale=200):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, 0, scale)  # Position the camera along the positive Z-axis
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin (or a point on the XY plane)
        camera.SetViewUp(0, -scale, 0)  # Set the up direction to be the negative Y-axis
        self.renderer.ResetCamera()  # Adjust the view to fit the scene
        self.vtk_widget.GetRenderWindow().Render()  # Render the scene with the new camera view

    def set_diagonal_view(self, scale=100):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(scale, scale, 0.5 * scale)  # Position the camera at an offset in X, Y, and Z
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin (or a central point in your scene)
        camera.SetViewUp(0, 0, scale)  # Set the up direction to be the Y-axis

        self.renderer.ResetCamera()  # Adjust the view to fit the scene
        self.vtk_widget.GetRenderWindow().Render()  # Render the scene with the new camera view

    def add_workspace_plane(self, width=200, height=200, grid_size=10):
        # Create a rectangular plane based on the given width and height
        half_width = width / 2.0
        half_height = height / 2.0
        plane = vtk.vtkPlaneSource()
        plane.SetOrigin(-half_width, -half_height, 0)
        plane.SetPoint1(half_width, -half_height, 0)
        plane.SetPoint2(-half_width, half_height, 0)
        plane.SetResolution(100, 100)  # This will create a grid pattern on the plane
        # Set the grid resolution based on the grid size
        plane.SetResolution(int(width / grid_size), int(height / grid_size))

        # Map the plane to a grid
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetEdgeColor(0.1, 0.1, 0.1)  # Set grid color
        actor.GetProperty().EdgeVisibilityOn()  # Show grid

        # Add the plane to the renderer
        self.renderer.AddActor(actor)
        # Add the plane to the renderer
        self.renderer.AddActor(actor)

    def clear_view(self):
        self.renderer.RemoveAllViewProps()
        # Update the renderer to reflect the changes
        self.vtk_widget.GetRenderWindow().Render()

        # Recreate workspace
        self.add_workspace_plane()
        self.set_diagonal_view()

