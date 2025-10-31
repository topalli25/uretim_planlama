"""
VTK tabanlı 3D görselleştirme widget'ı
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk


class GorunumWidget(QWidget):
    """VTK 3D görüntüleyici widget"""

    def __init__(self, parent=None):
        super().__init__(parent)

        try:
            # Ana layout
            self.layout = QVBoxLayout(self)
            self.layout.setContentsMargins(0, 0, 0, 0)

            # VTK widget
            print("   [DEBUG] QVTKRenderWindowInteractor oluşturuluyor...")
            self.vtk_widget = QVTKRenderWindowInteractor(self)
            self.layout.addWidget(self.vtk_widget)
            print("   [DEBUG] VTK widget eklendi")

            # Renderer
            print("   [DEBUG] Renderer oluşturuluyor...")
            self.renderer = vtk.vtkRenderer()
            self.renderer.SetBackground(0.2, 0.3, 0.4)  # Arka plan rengi

            # Render window
            print("   [DEBUG] Render window alınıyor...")
            self.render_window = self.vtk_widget.GetRenderWindow()
            self.render_window.AddRenderer(self.renderer)

            # Interactor
            print("   [DEBUG] Interactor ayarlanıyor...")
            self.interactor = self.render_window.GetInteractor()
            self.interactor_stili = vtk.vtkInteractorStyleTrackballCamera()
            self.interactor.SetInteractorStyle(self.interactor_stili)

            # Aktörler sözlüğü (parca_id: actor)
            self.aktorler = {}

            # Kamera ayarları
            print("   [DEBUG] Kamera ayarlanıyor...")
            self.kamerayi_ayarla()

            # Initialize
            print("   [DEBUG] Interactor Initialize ediliyor...")
            self.interactor.Initialize()
            print("   [DEBUG] GorunumWidget başarıyla oluşturuldu")

        except Exception as e:
            print(f"\n   [HATA] GorunumWidget oluşturulurken hata:")
            print(f"   [HATA] {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise

    def kamerayi_ayarla(self):
        """Kamera başlangıç ayarları"""
        kamera = self.renderer.GetActiveCamera()
        kamera.SetPosition(100, 100, 100)
        kamera.SetFocalPoint(0, 0, 0)
        kamera.SetViewUp(0, 0, 1)
        self.renderer.ResetCamera()

    def mesh_ekle(self, parca_id, mesh, renk=(0.8, 0.8, 0.8), opaklık=1.0):
        """
        Trimesh nesnesini sahneye ekle

        Args:
            parca_id (str): Parça ID
            mesh (trimesh.Trimesh): 3D mesh
            renk (tuple): RGB renk (0-1 arası)
            opaklık (float): Opaklık (0-1 arası)
        """
        # Trimesh'i VTK'ya dönüştür
        noktalar = mesh.vertices
        yuzeyler = mesh.faces

        # VTK Points
        vtk_noktalar = vtk.vtkPoints()
        for nokta in noktalar:
            vtk_noktalar.InsertNextPoint(nokta)

        # VTK Cells
        vtk_hucreler = vtk.vtkCellArray()
        for yuzey in yuzeyler:
            ucgen = vtk.vtkTriangle()
            ucgen.GetPointIds().SetId(0, yuzey[0])
            ucgen.GetPointIds().SetId(1, yuzey[1])
            ucgen.GetPointIds().SetId(2, yuzey[2])
            vtk_hucreler.InsertNextCell(ucgen)

        # PolyData
        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(vtk_noktalar)
        poly_data.SetPolys(vtk_hucreler)

        # Normals hesapla (daha iyi görünüm için)
        normaller = vtk.vtkPolyDataNormals()
        normaller.SetInputData(poly_data)
        normaller.ComputePointNormalsOn()
        normaller.Update()

        # Mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(normaller.GetOutputPort())

        # Actor
        aktor = vtk.vtkActor()
        aktor.SetMapper(mapper)
        aktor.GetProperty().SetColor(renk)
        aktor.GetProperty().SetOpacity(opaklık)

        # Sahneye ekle
        self.renderer.AddActor(aktor)
        self.aktorler[parca_id] = aktor

        # Render
        self.render_window.Render()

    def mesh_kaldir(self, parca_id):
        """Mesh'i sahneden kaldır"""
        if parca_id in self.aktorler:
            self.renderer.RemoveActor(self.aktorler[parca_id])
            del self.aktorler[parca_id]
            self.render_window.Render()

    def mesh_gorunurlugunu_ayarla(self, parca_id, gorunur):
        """Mesh görünürlüğünü ayarla"""
        if parca_id in self.aktorler:
            self.aktorler[parca_id].SetVisibility(gorunur)
            self.render_window.Render()

    def mesh_rengini_ayarla(self, parca_id, renk):
        """Mesh rengini değiştir"""
        if parca_id in self.aktorler:
            self.aktorler[parca_id].GetProperty().SetColor(renk)
            self.render_window.Render()

    def mesh_vurgula(self, parca_id, vurgula=True):
        """Mesh'i vurgula (parlak sarı renk)"""
        if parca_id in self.aktorler:
            if vurgula:
                self.aktorler[parca_id].GetProperty().SetColor(1.0, 1.0, 0.0)
                self.aktorler[parca_id].GetProperty().SetOpacity(1.0)
            else:
                # Orijinal renge dön (bu durumda gri)
                self.aktorler[parca_id].GetProperty().SetColor(0.8, 0.8, 0.8)
            self.render_window.Render()

    def sahneyi_temizle(self):
        """Tüm mesh'leri temizle"""
        for aktor in list(self.aktorler.values()):
            self.renderer.RemoveActor(aktor)
        self.aktorler.clear()
        self.render_window.Render()

    def kamerayi_sifirla(self):
        """Kamerayı sıfırla"""
        self.renderer.ResetCamera()
        self.render_window.Render()

    def kamera_pozisyonunu_ayarla(self, pozisyon, odak_noktasi=None):
        """
        Kamera pozisyonunu ayarla

        Args:
            pozisyon (list): [x, y, z] kamera pozisyonu
            odak_noktasi (list): [x, y, z] odak noktası (opsiyonel)
        """
        kamera = self.renderer.GetActiveCamera()
        kamera.SetPosition(pozisyon)
        if odak_noktasi:
            kamera.SetFocalPoint(odak_noktasi)
        self.renderer.ResetCamera()
        self.render_window.Render()

    def mesh_sayisi_al(self):
        """Sahnedeki mesh sayısı"""
        return len(self.aktorler)
