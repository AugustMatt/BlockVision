# Classe Viewer (herdando de QGraphicsView):

# Responsabilidade Principal: 
#   Exibir o conteúdo da cena (Workspace) e fornecer a interface para interação com a cena.

# Responsabilidades:
#   Exibir o QGraphicsScene (o workspace).
#   Gerenciar a interface do usuário para interações visuais, como zoom e rotação.
#   ENCAMINHAR eventos do usuário para o workspace.

# Funções Típicas: 
#   Atualizar a visualização da cena, 
#   lidar com a rotação e o zoom    
#   RESPONDER (não é lidar) a interações do usuário como cliques e arrastos.

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt
from workspace.workspace import Workspace
from nodes.node import Node

class Viewer(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = Workspace(self)
        self.setScene(self.scene)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scene.setBackgroundBrush(QBrush(QColor(200, 200, 200), Qt.SolidPattern))
        self.setRenderHint(QPainter.Antialiasing)

    def addItem(self, action, icon_path):
        self.scene.add(action.text(), icon_path)

    def setMode(self, action):
        self.scene.setMode(action.text())

    def run(self):
        circuit_item = self._get_selected_node()
        if circuit_item:
            circuit_item.run()
        else:
            print("Selected item is not a circuit item or no item selected")

    def openOptionsWindow(self):
        circuit_item = self._get_selected_node()
        if circuit_item:
            circuit_item.optionsWindow()
        else:
            print("Selected item is not a circuit item or no item selected")

    def _get_selected_node(self):
        """
        Retrieves the selected item from the scene and checks if it is a Node.
        Returns:
            Node: The selected Node if valid, otherwise None.
        """
        selected_items_list = self.scene.selectedItems()
        if selected_items_list:
            selected_item = selected_items_list[0]
            return selected_item if isinstance(selected_item, Node) else None
        return None