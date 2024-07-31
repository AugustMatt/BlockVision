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

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Adicione lógica adicional se necessário

    # Adiciona o bloco funcional a cena utilizando o metodo add da classe circuitscene
    def addItem(self, action, icon_path):
        self.scene.add(action.text(), icon_path)

    # Ajusta o modo de interação conforme necessário
    def setMode(self, action):
        self.scene.setMode(action.text())

    # Executa a funcionalidade do bloco selecionado
    def play(self):

        # Lista dos elementos selecionados
        # Espera-se ter somente um (indice 0)
        selected_items_list = self.scene.selectedItems()
        
        # Se existe ao menos um item selecionado
        if selected_items_list:

            # Adquire esse item
            selected_item = selected_items_list[0]

            # Verifica se é do tipo circuit item, caso contrario o substitui por None
            circuit_item = selected_item if isinstance(selected_item, Node) else None

            # Caso exista
            if circuit_item:
                circuit_item.run()
            else:
                print("Elemento selecionado não é um circuit item")
        else:
            print("Sem elementos selecionados")

    # Abre a janela de ajustes do bloco funcional selecionado (Se houver)
    def openOptionsWindow(self):
        
        # Lista dos elementos selecionados
        # Espera-se ter somente um (indice 0)
        selected_items_list = self.scene.selectedItems()

        # Se existe ao menos um item selecionado
        if selected_items_list:

            # Adquire esse item
            selected_item = selected_items_list[0]

            # Verifica se é do tipo circuit item, caso contrario o substitui por None
            circuit_item = selected_item if isinstance(selected_item, Node) else None

            # Caso exista
            if circuit_item:                
                circuit_item.optionsWindow()
            else:
                print("Elemento selecionado não é um circuit item")

        else:
            print("Sem elementos selecionados")