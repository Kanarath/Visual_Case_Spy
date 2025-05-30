# visual_case_spy/ui/main_window.py
import uuid
from PySide6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QToolBar
from PySide6.QtGui import QPainter, QAction, QIcon # QIcon es para más tarde, QPainter ya estaba
from PySide6.QtCore import Slot, Qt
from .node_item import NodeItem # Asegúrate de que node_item.py esté en el mismo directorio 'ui'

print("DEBUG: main_window.py - Module imported")

class VCSGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("DEBUG: VCSGraphicsScene - __init__ called")
        # Configuraciones adicionales de la escena si son necesarias
        # self.setSceneRect(-2000, -2000, 4000, 4000) # Movido a MainWindow para asegurar que se llame después de la creación

class VCSGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        print("DEBUG: VCSGraphicsView - __init__ called")
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        # Otras configuraciones: zoom, etc.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("DEBUG: MainWindow - __init__ started")
        self.setWindowTitle("Visual Case Spy - MVP")
        self.setGeometry(100, 100, 1024, 768)

        self.scene = VCSGraphicsScene(self) # Pasamos self como parent
        print("DEBUG: MainWindow - VCSGraphicsScene instance created")
        # Es importante establecer el sceneRect DESPUÉS de crear la escena
        self.scene.setSceneRect(-2000, -2000, 4000, 4000) 
        print("DEBUG: MainWindow - SceneRect set for self.scene")

        self.view = VCSGraphicsView(self.scene, self) # Pasamos self como parent
        print("DEBUG: MainWindow - VCSGraphicsView instance created")
        
        self.setCentralWidget(self.view)
        print("DEBUG: MainWindow - Central widget set to self.view")

        self.node_counter = 0

        self._create_actions()
        print("DEBUG: MainWindow - _create_actions() called and returned")
        self._create_toolbars()
        print("DEBUG: MainWindow - _create_toolbars() called and returned")
        
        print("DEBUG: MainWindow - __init__ finished")

    def _create_actions(self):
        print("DEBUG: MainWindow - _create_actions() entered")
        # Acción para añadir un nodo
        self.add_node_action = QAction("Add Node", self) # self aquí es el parent (MainWindow)
        # self.add_node_action.setIcon(QIcon("path/to/add_node_icon.png"))
        self.add_node_action.setToolTip("Add a new generic node to the canvas")
        self.add_node_action.triggered.connect(self.on_add_node)
        print("DEBUG: MainWindow - _create_actions() finished")

    def _create_toolbars(self):
        print("DEBUG: MainWindow - _create_toolbars() entered")
        # Barra de herramientas de edición
        edit_toolbar = QToolBar("Edit Toolbar", self) # self aquí es el parent (MainWindow)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, edit_toolbar)
        edit_toolbar.addAction(self.add_node_action)
        print("DEBUG: MainWindow - _create_toolbars() finished")

    @Slot()
    def on_add_node(self):
        print("DEBUG: MainWindow - on_add_node() called")
        self.node_counter += 1
        node_id = str(uuid.uuid4())
        label = f"Node {self.node_counter}"
        node_type = "GEN" # Tipo genérico por ahora

        # Asumimos que NodeItem está definido correctamente en node_item.py
        new_node = NodeItem(node_id=node_id, label=label, node_type=node_type)
        
        # Calcular una posición inicial
        # Podrías mapear la vista al centro de la escena la primera vez o usar el centro de la vista actual
        # view_center = self.view.mapToScene(self.view.viewport().rect().center())
        # initial_x = view_center.x() + (self.node_counter % 5 - 2) * (new_node.width + 20)
        # initial_y = view_center.y() + (self.node_counter // 5 - 1) * (new_node.height + 20)
        
        # O una posición más simple relativa al origen de la escena por ahora:
        initial_x = (self.node_counter % 10) * (new_node.width + 10) - (5 * (new_node.width + 10)) # Para esparcirlos un poco
        initial_y = (self.node_counter // 10) * (new_node.height + 10)


        new_node.setPos(initial_x, initial_y)
        self.scene.addItem(new_node)
        print(f"DEBUG: Added node: {new_node} at scene pos ({initial_x}, {initial_y})")