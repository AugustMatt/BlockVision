# Classe Workspace (herdando de QGraphicsScene):

# Responsabilidade Principal: 
#   Gerenciar e organizar os itens dentro da cena (dele mesmo), como blocos funcionais e conexões entre eles.

# Responsabilidades:
#   Gerenciar os itens na cena, como blocos e conexões.
#   Lidar com eventos específicos da cena, como cliques e movimentações.
#   Fornecer métodos para adicionar, remover e conectar itens.

# Funções Típicas: 
#   Adicionar, remover e conectar itens; 
#   Gerenciar (lidar) eventos dentro da cena, como cliques e arrastos.

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem
from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QTransform
from nodes.node import Node
from nodes.load_image import LoadImage
from nodes.display_image import DisplayImage
from nodes.convolution_kernel import ConvolutionKernel
from nodes.convolution import Convolution
from nodes.connector import Connector
from nodes.add import Add

class Workspace(QGraphicsScene):
    """
    Manages and organizes items within the scene, such as functional blocks and connections between them.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mode = "Point"
        self.line = None

    def mousePressEvent(self, event):
        """
        Handles mouse press events. Initiates line creation if in LINE mode, 
        or allows item selection if in POINTER mode.
        """
        if event.button() == Qt.LeftButton:
            if self.mode == "Line":
                self.line = QGraphicsLineItem(QLineF(event.scenePos(), event.scenePos()))
                self.addItem(self.line)
            elif self.mode == "Point":
                if not self.itemAt(event.scenePos(), QTransform()):
                    self.clearSelection()
                super().mousePressEvent(event)
            else:
                raise ValueError('Unknown scene operation mode')

    def mouseMoveEvent(self, event):
        """
        Updates the line being drawn as the mouse moves in LINE mode.
        """
        if self.line and self.mode == "Line":
            new_line = QLineF(self.line.line().p1(), event.scenePos())
            self.line.setLine(new_line)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Finalizes the line connection or processes item placement when the mouse is released.
        """
        if self.line and self.mode == "Line":
            self._process_line_end(event)
        super().mouseReleaseEvent(event)

    def _process_line_end(self, event):
        """
        Processes the end of a line connection, including validating and creating a Connector.
        """
        start_items = self.items(self.line.line().p1())
        end_items = self.items(self.line.line().p2())
        start_item = next((item for item in start_items if isinstance(item, Node)), None)
        end_item = next((item for item in end_items if isinstance(item, Node)), None)

        self.removeItem(self.line)
        del self.line
        self.line = None

        if start_item and end_item and start_item != end_item:
            if self._connection_exists(start_item, end_item):
                print("Connection already exists between blocks!")
                return

            if not self._can_connect(start_item, end_item):
                return

            connector = Connector(start_item, end_item)
            self.addItem(connector)
            start_item.addOutputConnector(connector)
            end_item.addInputConnector(connector)
            connector.setZValue(-1)
        else:
            print("Invalid connection or same start and end item.")

    def _connection_exists(self, start_item, end_item):
        """
        Checks if a connection already exists between the given start and end items.
        """
        return any(connector.getDst() == end_item for connector in start_item.output_connectors)

    def _can_connect(self, start_item, end_item):
        """
        Checks if the start and end items can be connected based on their types and positions.
        """
        if start_item.getType() == "Display Image":
            print("Display Image block cannot be a source")
            return False
        elif end_item.getType() == "Load Image":
            print("Load Image block cannot have inputs")
            return False
        elif end_item.getType() == "Display Image" and len(end_item.getInputConnectors()) >= 1:
            print("Display Image block can only have one input")
            return False
        elif end_item.getType() == "Add" and len(end_item.getInputConnectors()) >= 2:
            print("Sum images block can only have two inputs")
            return False
        elif self.checkBlockCollision(start_item, end_item):
            print("Blocks collide; connector will not be added")
            return False
        return True

    def add(self, node_type, icon_path):
        """
        Adds a new item to the scene based on the specified node type.
        """
        node_classes = {
            "Load Image": LoadImage,
            "Display Image": DisplayImage,
            "Convolution Kernel": ConvolutionKernel,
            "Convolution": Convolution,
            "Add": Add
        }

        if node_type in node_classes:
            node_class = node_classes[node_type]
            item = node_class(icon_path)
            self.addItem(item)
            self._deselect_all_items()
            item.setSelected(True)
        else:
            print(f"Unknown node type: {node_type}")

    def _deselect_all_items(self):
        """
        Deselects all items in the scene.
        """
        for item in self.selectedItems():
            item.setSelected(False)

    def setMode(self, mode):
        """
        Sets the scene operation mode and deselects all items.
        """
        self._deselect_all_items()
        if mode in ["Line", "Point"]:
            self.mode = mode
        else:
            raise ValueError("Unknown mode: {}".format(mode))

    def isItemChange(self, type):
        """
        Checks if any selected item matches the specified type.
        """
        return any(item.type() == type for item in self.selectedItems())

    def checkBlockCollision(self, start_item, end_item):
        """
        Checks if two items are colliding.
        """
        return start_item.collidesWithItem(end_item)

    def keyPressEvent(self, event):
        """
        Handles key press events. Deletes selected connectors if the Delete key is pressed.
        """
        if event.key() == Qt.Key_Delete:
            self.delete_selected_items()
            
    def delete_selected_items(self):
        """
        Deletes all selected items. Supports deleting blocks and their associated connectors.
        """
        for item in self.selectedItems():
            try:
                item.remove()
            except Exception as e:
                print(f'Error on trying delete: {e}')
