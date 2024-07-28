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
from nodes.connector import Connector

class Workspace(QGraphicsScene):

    def __init__(self, parent=None):

        super().__init__(parent)

        # Modo de operação da cena
        # Possiveis valores:
        #   POINTER -> habilita selecionar, arrastar e soltar blocos no diagrama
        #   LINE -> habilita a criação de linhas de conexões entre os blocos no diagrama
        self.mode = "POINTER"

        # Acho que essa variavel não esta sendo usada, verificar depois
        self.item = None

        # Atributo que ira armazenar a "linha fantasma" que aparece durante a criação de uma conexão
        self.line = None

    # Ao pressionar o botão do mouse na cena
    def mousePressEvent(self, event):

        # Se for o botão esquerdo do mouse
        if event.button() == Qt.LeftButton:

            # Se o modo de conexão entre blocos estiver ativado
            if self.mode == "LINE":
                self.line = QGraphicsLineItem(QLineF(event.scenePos(), event.scenePos()))
                self.addItem(self.line)
            
            # Caso contrario (até o momento seria o modo de arrastar/soltar/selecionar blocos)
            elif self.mode == "POINTER":

                # Desmarcar todos os itens atualmente selecionados
                if not self.itemAt(event.scenePos(), QTransform()):
                    self.clearSelection()

                # Permitir seleção de itens existentes
                super().mousePressEvent(event)
            
            else:
                raise('Modo de operação da cena desconhecido')

    # Evento de mover o mouse
    def mouseMoveEvent(self, event):

        # Se existir uma linha a ser criada e o modo de operação for o de criação de conexão, redesenha a linha usando a posição do
        # cursor do mouse como ponto final
        if self.line is not None and self.mode == "LINE":
            new_line = QLineF(self.line.line().p1(), event.scenePos())
            self.line.setLine(new_line)
        else:
            super().mouseMoveEvent(event)
  
    # Ao soltar o botão do mouse na cena
    def mouseReleaseEvent(self, event):

        # Se houver uma linha para ser criada e estiver no modo de criação de conexão
        if self.line is not None and self.mode == "LINE":

            # Obtém os blocos presentes na posição inicial e final da linha
            # obs, aqui retorna tanto os objetos do tipo circuit item quanto os objetos do tipo line
            start_items = self.items(self.line.line().p1())
            end_items = self.items(self.line.line().p2())

            # Dado que uma linha so tem um circuit item de entrada e um de saida
            # Filtramos apenas os circuit itens
            start_item = next((item for item in start_items if isinstance(item, Node)), None)
            end_item = next((item for item in end_items if isinstance(item, Node)), None)

            # Apaga a linha fantasma
            self.removeItem(self.line)
            del self.line
            self.line = None

            if start_item and end_item and start_item != end_item:

                # Verifica se já existe uma conexão entre o bloco de entrada (start_item) e o bloco de saída (end_item)

                # Itera sobre todos os conectores de saída do bloco de entrada (start_item)
                # Para cada conector, verifica se o bloco de destino (dst) do conector é igual ao bloco de saída (end_item)
                existing_connection = any(
                    connector.getDst() == end_item  # Compara o bloco de destino do conector com o bloco de saída
                    for connector in start_item.output_connectors  # Itera sobre todos os conectores de saída do bloco de entrada
                )

                if existing_connection:
                    print("Conexão já existe entre os blocos!")
                    return

                # Verificações específicas por tipo do bloco

                # O bloco de exibir imagem não pode servir de entrada
                if start_item.getType() == "Display Image":
                    print("Bloco de exibir imagem não pode ser uma entrada")
                    return
                
                # O bloco para carregar imagem não pode conter uma entrada
                elif end_item.getType() == "Load Image":
                    print("Bloco de carregar imagem não pode conter entradas")
                    return
                
                # O bloco de exibir imagem so pode conter uma entrada no maximo
                elif end_item.getType() == "Display Image" and len(end_item.getInputConnectors()) >= 1:
                    print("Bloco de exibir imagem so pode conter uma entrada no maximo")
                    return
                
                # Para evitar problema de calculos, os blocos os quais o conector irá conectar, não podem estar colidindo
                elif self.checkBlockCollision(start_item, end_item):
                    print("Blocos colidem e o conector não será adicionado")
                    return
                
                # Cria e adiciona o conector a cena
                else:
                    connector = Connector(start_item, end_item)
                    self.addItem(connector)
                    start_item.addOutputConnector(connector)
                    end_item.addInputConnector(connector)
                    connector.setZValue(-1)
           
            else:
                print("Conexão não pode ser criada. Itens de início e fim não são válidos ou são os mesmos.")

        super().mouseReleaseEvent(event)

    # Cria uma instancia de circuititem com base no texto (s) do action clicado
    # Note que o metodo addItem vem da classe pai QGraphicsScene via herança
    def add(self, node_type, icon_path):
        item = Node(node_type, icon_path)
        self.addItem(item)

        # Deseleciona todos os blocos quando o modo é trocado
        for another_item in self.selectedItems():
            another_item.setSelected(False)
        item.setSelected(True)

    # Troca o modo de operação da cena
    # É chamada é mainwindow.py
    def setMode(self, s):

        # Deseleciona todos os blocos quando o modo é trocado
        for item in self.selectedItems():
            item.setSelected(False)

        if s == "LINE":
            self.mode = "LINE"
        else:
            self.mode = "POINTER"

    def isItemChange(self, type):
        for item in self.selectedItems():
            if item.type() == type:
                return True
        return False
    
    def record(self, filename):
        myitems = self.items()
        for count, item in enumerate(myitems):
            print(f"count = {count}")
            if isinstance(item, Node):
                print(f"item {item.getType()}")

    # Metodo que verifica se dois objetos estão colidindo
    # Usado durante a criação de conexão para evitar problemas
    def checkBlockCollision(self, start_item, end_item):
        if start_item.collidesWithItem(end_item):
            return True
        return False

    # Evento de pressionamento de tecla
    def keyPressEvent(self, event):

        # Se a tecla delete for pressionada, chama o metodo para deleção de um connector (caso este seja o elemento selecionado)
        if event.key() == Qt.Key_Delete:
            self.delete_selected_items()

    def delete_selected_items(self):
        for item in self.selectedItems():
            if isinstance(item, Connector):
                item.remove()
            else:
                print('Deleção de blocos ainda não implementada')
                return




            