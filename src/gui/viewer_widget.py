"""
VTK tabanlı 3D görselleştirme widget'ı
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk


class VTKViewerWidget(QWidget):
    """VTK 3D görüntüleyici widget"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Ana layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # VTK widget
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.layout.addWidget(self.vtk_widget)

        # Renderer
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.2, 0.3, 0.4)  # Arka plan rengi

        # Render window
        self.render_window = self.vtk_widget.GetRenderWindow()
        self.render_window.AddRenderer(self.renderer)

        # Interactor
        self.interactor = self.render_window.GetInteractor()
        self.interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(self.interactor_style)

        # Aktörler sözlüğü (parça_id: actor)
        self.actors = {}

        # Kamera ayarları
        self.setup_camera()

        # Initialize
        self.interactor.Initialize()

    def setup_camera(self):
        """Kamera başlangıç ayarları"""
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(100, 100, 100)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 0, 1)
        self.renderer.ResetCamera()

    def add_mesh(self, part_id, mesh, color=(0.8, 0.8, 0.8), opacity=1.0):
        """
        Trimesh nesnesini sahneye ekle

        Args:
            part_id (str): Parça ID
            mesh (trimesh.Trimesh): 3D mesh
            color (tuple): RGB renk (0-1 arası)
            opacity (float): Opaklık (0-1 arası)
        """
        # Trimesh'i VTK'ya dönüştür
        vertices = mesh.vertices
        faces = mesh.faces

        # VTK Points
        vtk_points = vtk.vtkPoints()
        for vertex in vertices:
            vtk_points.InsertNextPoint(vertex)

        # VTK Cells
        vtk_cells = vtk.vtkCellArray()
        for face in faces:
            triangle = vtk.vtkTriangle()
            triangle.GetPointIds().SetId(0, face[0])
            triangle.GetPointIds().SetId(1, face[1])
            triangle.GetPointIds().SetId(2, face[2])
            vtk_cells.InsertNextCell(triangle)

        # PolyData
        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(vtk_points)
        poly_data.SetPolys(vtk_cells)

        # Normals hesapla (daha iyi görünüm için)
        normals = vtk.vtkPolyDataNormals()
        normals.SetInputData(poly_data)
        normals.ComputePointNormalsOn()
        normals.Update()

        # Mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(normals.GetOutputPort())

        # Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(opacity)

        # Sahneye ekle
        self.renderer.AddActor(actor)
        self.actors[part_id] = actor

        # Render
        self.render_window.Render()

    def remove_mesh(self, part_id):
        """Mesh'i sahneden kaldır"""
        if part_id in self.actors:
            self.renderer.RemoveActor(self.actors[part_id])
            del self.actors[part_id]
            self.render_window.Render()

    def set_mesh_visibility(self, part_id, visible):
        """Mesh görünürlüğünü ayarla"""
        if part_id in self.actors:
            self.actors[part_id].SetVisibility(visible)
            self.render_window.Render()

    def set_mesh_color(self, part_id, color):
        """Mesh rengini değiştir"""
        if part_id in self.actors:
            self.actors[part_id].GetProperty().SetColor(color)
            self.render_window.Render()

    def highlight_mesh(self, part_id, highlight=True):
        """Mesh'i vurgula (parlak sarı renk)"""
        if part_id in self.actors:
            if highlight:
                self.actors[part_id].GetProperty().SetColor(1.0, 1.0, 0.0)
                self.actors[part_id].GetProperty().SetOpacity(1.0)
            else:
                # Orijinal renge dön (bu durumda gri)
                self.actors[part_id].GetProperty().SetColor(0.8, 0.8, 0.8)
            self.render_window.Render()

    def clear_scene(self):
        """Tüm mesh'leri temizle"""
        for actor in list(self.actors.values()):
            self.renderer.RemoveActor(actor)
        self.actors.clear()
        self.render_window.Render()

    def reset_camera(self):
        """Kamerayı sıfırla"""
        self.renderer.ResetCamera()
        self.render_window.Render()

    def set_camera_position(self, position, focal_point=None):
        """
        Kamera pozisyonunu ayarla

        Args:
            position (list): [x, y, z] kamera pozisyonu
            focal_point (list): [x, y, z] odak noktası (opsiyonel)
        """
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(position)
        if focal_point:
            camera.SetFocalPoint(focal_point)
        self.renderer.ResetCamera()
        self.render_window.Render()

    def get_mesh_count(self):
        """Sahnedeki mesh sayısı"""
        return len(self.actors)
