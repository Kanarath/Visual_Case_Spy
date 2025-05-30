# visual_case_spy/ui/node_item.py
from PySide6.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget # QGraphicsRectItem y QGraphicsTextItem no se usan si pintas manualmente
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PySide6.QtCore import Qt, QRectF

class NodeItem(QGraphicsItem):
    def __init__(self, node_id, label="Node", node_type="GEN", parent=None): # parent=None es importante para QGraphicsItem
        super().__init__(parent) # No pasar parent si es un item de nivel superior en la escena
        
        # Es buena práctica que los QGraphicsItems no tengan parent si van a ser añadidos directamente a la escena
        # y gestionados por la escena. Si fueran hijos de OTRO QGraphicsItem, entonces sí se pasaría el parent.
        # Para los nodos en nuestra escena, parent es None.

        self.node_id = node_id
        self.label_text = label
        self.node_type_text = node_type

        # Dimensiones y apariencia básica
        self.width = 120
        self.height = 60
        self.color_background = QColor("#5DADE2")
        self.color_border = QColor("#1A5276")
        self.color_text = QColor(Qt.black) # Qt.black ya está definido en Qt.GlobalColor
        self.color_type_text = QColor(Qt.darkGray) # Qt.darkGray también está definido

        # Elementos para dibujar: rect y texto
        self.rect = QRectF(0, 0, self.width, self.height) # Origen local en (0,0)
        
        # Hacer el item seleccionable y movible
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        # Cache para mejorar el rendimiento del dibujado
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

    def boundingRect(self) -> QRectF:
        pen_width = 1.0 
        return self.rect.adjusted(-pen_width / 2, -pen_width / 2, pen_width / 2, pen_width / 2)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        painter.setBrush(QBrush(self.color_background))
        
        pen = QPen(self.color_border)
        pen.setWidth(1) # El ancho de la pluma debe ser un número
        painter.setPen(pen)
        painter.drawRect(self.rect)

        painter.setPen(self.color_type_text)
        type_font = QFont("Arial", 8)
        painter.setFont(type_font)
        type_text_rect = QRectF(self.rect.left() + 5, self.rect.top() + 2, self.width - 10, 15)
        painter.drawText(type_text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, self.node_type_text)

        painter.setPen(self.color_text)
        label_font = QFont("Arial", 10, QFont.Weight.Bold) # Usar QFont.Weight.Bold
        painter.setFont(label_font)
        label_rect = QRectF(self.rect.left() + 5, self.rect.top() + 20, self.width - 10, self.height - 25)
        painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.TextWordWrap, self.label_text)

    def __repr__(self):
        return f"<NodeItem id='{self.node_id}' label='{self.label_text}'>"