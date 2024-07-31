# Classe que representa uma conexão entre dois blocos funcionais da aplicação
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt, QSizeF

class Connector(QGraphicsLineItem):
    """
    Represents a connection between two functional blocks in the application.
    """

    def __init__(self, src, dst, parent=None, scene=None):
        """
        Initializes the Connector with source and destination items.

        :param src: Source item of the connection.
        :param dst: Destination item of the connection.
        :param parent: Parent item in the scene.
        :param scene: The scene to which the connector belongs.
        """
        super().__init__(parent)

        self.src = src
        self.dst = dst
        self.radius = 10
        self.line_color = QColor(Qt.black)
        self.circle_color = QColor(Qt.red)

        self.setZValue(0)
        self.setFlags(QGraphicsLineItem.ItemIsSelectable)

        self.updatePosition()

    def paint(self, painter, option, widget):
        """
        Paints the connector line and the end circle.

        :param painter: The QPainter object used for drawing.
        :param option: The style options for the item.
        :param widget: The widget on which the item is being painted.
        """
        self.updatePosition()

        pen = QPen(self.line_color)
        pen.setWidth(3)
        if self.isSelected():
            pen.setColor(Qt.blue)
        painter.setPen(pen)

        painter.setBrush(self.circle_color)
        painter.drawLine(self.center_line)
        painter.drawEllipse(self.border_point, self.radius, self.radius)

    def boundingRect(self):
        """
        Returns the bounding rectangle of the connector.

        :return: QRectF bounding rectangle of the connector.
        """
        extra = (self.pen().width() + 20) / 2.0 + self.radius
        return QRectF(self.line().p1(), QSizeF(self.line().p2().x() - self.line().p1().x(), self.line().p2().y() - self.line().p1().y())).normalized().adjusted(-extra, -extra, extra, extra)

    def updatePosition(self):
        """
        Updates the position and length of the connector based on source and destination items.
        """
        src_center = self.src.center()
        dst_center = self.dst.center()

        self.center_line = QLineF(src_center, dst_center)
        self.border_vector = self.center_line.unitVector()

        self.dst_width = 0.5 * self.dst.boundingRect().width()
        self.dst_height = 0.5 * self.dst.boundingRect().height()

        self.border_point = QPointF(
            -self.dst_width * self.border_vector.dx() + dst_center.x(),
            -self.dst_height * self.border_vector.dy() + dst_center.y()
        )
        self.setLine(QLineF(src_center, self.border_point))

    def getSrc(self):
        """
        Returns the source item of the connection.

        :return: Source item.
        """
        return self.src

    def getDst(self):
        """
        Returns the destination item of the connection.

        :return: Destination item.
        """
        return self.dst

    def remove(self):
        """
        Removes the connector from the source and destination items' connector lists and the scene.
        """
        # Remover o conector das listas de conectores dos itens
        if self in self.src.output_connectors:
            self.src.output_connectors.remove(self)
        if self in self.dst.input_connectors:
            self.dst.input_connectors.remove(self)
        
        # Remover referências aos itens conectados
        self.src = None
        self.dst = None
        
        # Remover o conector da cena
        if self.scene() is not None:
            self.scene().removeItem(self)