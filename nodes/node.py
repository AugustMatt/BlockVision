# Classe base dos blocos funcionais
# Possui todos os atributos e metodos em comum a todos os blocos funcionais
# A classe connector esta no mesmo diretorio mas não é um bloco funcional
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QPainterPath, QFont
from PyQt5.QtCore import QRectF, QPointF, Qt


class Node(QGraphicsItem):
    
    def __init__(self, item_type):
        super().__init__()

        # Type and name of the block
        # The name will be written below the block
        self.item_type = item_type
        self.item_name = item_type

        # Dimensions in pixels of the block
        self.width = 85
        self.height = 85

        # Font size for the block name
        self.font = QFont()
        self.font.setPointSize(8)

        # Height in pixels of the block name text box
        self.text_height_in_pixels = 16

        # Lists of input and output connectors for the block
        self.input_connectors = []
        self.output_connectors = []

        # Makes the block movable, selectable, etc.
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def paint(self, painter, option, widget):
        """
        Renders the block's name (below it).
        Draws the block border if selected.
        """
        painter.setPen(QPen(Qt.black))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.setFont(self.font)
        
        # Draw the text below the block
        text_rect = QRectF(0, 0, self.width, self.height)
        text_rect.setHeight(self.height + self.text_height_in_pixels)
        painter.drawText(text_rect, Qt.AlignBottom | Qt.AlignHCenter, self.item_name)
        
        # Draw the block border if selected
        if self.isSelected():
            painter.setPen(QPen(Qt.blue))
        else:
            painter.setPen(QPen(Qt.transparent))

        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawRect(self.boundingRect())
        self.update()

    def run(self):
        """
        Executes the block's functionalities.
        Some functional blocks will have their own run methods (polymorphism).
        For those that do not, just prints a message to the terminal.
        """
        print("Run method not implemented for this block")

    def optionsWindow(self):
        """
        Creates and renders the block's options window.
        Some functional blocks will have their own optionsWindow methods (polymorphism).
        For those that do not, just prints a message to the terminal.
        """
        print("Options window not implemented for this block")

    def boundingRect(self):
        """
        Returns the bounding box of the block with additional height for the block's name text.
        """
        return QRectF(0, 0, self.width, self.height + self.text_height_in_pixels)

    def itemChange(self, change, value):
        """
        Called when the block is moved.
        Updates the position of the block's connectors.
        """
        if change == QGraphicsItem.ItemPositionChange:
            for connector in self.input_connectors:
                connector.updatePosition()
            
            for connector in self.output_connectors:
                connector.updatePosition()
        
        return super().itemChange(change, value)

    def center(self):
        """
        Returns the center point of the functional block.
        Used by the Connector class.
        """
        return QPointF(self.x() + self.width / 2, self.y() + self.height / 2)

    def shape(self):
        """
        Returns the shape of the block for collision detection.
        """
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def getType(self):
        """
        Returns the type of the functional block.
        """
        return self.item_type

    def addInputConnector(self, connector):
        """
        Adds a connector to the block's list of input connectors.
        """
        self.input_connectors.append(connector)

    def addOutputConnector(self, connector):
        """
        Adds a connector to the block's list of output connectors.
        """
        self.output_connectors.append(connector)

    def getInputConnectors(self):
        """
        Returns the list of input connectors.
        """
        return self.input_connectors

    def removeInputConnector(self, connector):
        """
        Removes a specific input connector from the block's list of input connectors.
        """
        self.input_connectors.remove(connector)

    def removeOutputConnector(self, connector):
        """
        Removes a specific output connector from the block's list of output connectors.
        """
        self.output_connectors.remove(connector)

    def remove(self):
        """
        Removes a block and all its associated connectors.
        """
        # Remove todas as conexões associadas ao bloco
        for connector in self.input_connectors + self.output_connectors:
            connector.remove()
        
        # Remove o bloco da cena
        self.scene().removeItem(self)