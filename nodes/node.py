# Classe base dos blocos funcionais
# Possui todos os atributos e metodos em comum a todos os blocos funcionais
# A classe connector esta no mesmo diretorio mas não é um bloco funcional
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QPainterPath, QFont
from PyQt5.QtCore import QRectF, QPointF, Qt

class Node(QGraphicsItem):
    
    def __init__(self, item_type):
        super().__init__()

        # Tipo e nome do bloco
        # O nome sera escrito abaixo do bloco
        self.item_type = item_type
        self.item_name = item_type

        # Dimensões em pixels do bloco
        self.width = 85
        self.height = 85

        # Tamanho da fonte do nome do bloco
        self.font = QFont()
        self.font.setPointSize(8)

        # Altura em pixels da caixa de texto do nome do bloco
        self.text_height_in_pixels = 16

        # Listas com os conectores de entrada e saida que do bloco
        self.input_connectors = []
        self.output_connectors = []

        # Faz o bloco ser deslocavel, selecionavel e ...
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    # Metodo para renderizar o nome do bloco (abaixo dele)
    def paint(self, painter, option, widget):

        painter.setPen(QPen(Qt.black))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.setFont(self.font)
        
        # Desenha o texto abaixo do bloco
        text_rect = QRectF(0, 0, self.width, self.height)
        text_rect.setHeight(self.height + self.text_height_in_pixels)
        painter.drawText(text_rect, Qt.AlignBottom | Qt.AlignHCenter, self.item_name)
        
        # Desenha a borda do bloco se estiver selecionado
        if self.isSelected():
            painter.setPen(QPen(Qt.blue))
        else:
            painter.setPen(QPen(Qt.transparent))

        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawRect(self.boundingRect())
        self.update()

    # Metodo que executa as funcionalidades do bloco funcional
    # Alguns blocos funcionais terão seus proprios metodos run (polimorfismo)
    # Para os que não tiverem, exibe apenas uma mensagem no terminal
    def run(self):
        print("Metodo de execução não implementado para esse bloco")

    # Metodo que cria e renderiza a janela de opções desse bloco
    # Alguns blocos funcionais terão seus proprios metodos optionsWindow (polimorfismo)
    # Para os que não tiverem, exibe apenas uma mensagem no terminal
    def optionsWindow(self):
        print("Janela de configurações não implementada para esse bloco")

    # Retorna caixa delimitadora do bloco com um acresimo na altura para o texto que representa o nome do blocos
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height + self.text_height_in_pixels)

    # Metodo executado quando ocorre um deslocamento no bloco
    # Atualiza a posição dos conectores do bloco
    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemPositionChange:

            for connector in self.input_connectors:
                connector.updatePosition()
            
            for connector in self.output_connectors:
                connector.updatePosition()
        
        return super().itemChange(change, value)

    # Retorna o ponto central do bloco funcional
    # Usado pela classe connector
    def center(self):
        return QPointF(self.x() + self.width / 2, self.y() + self.height / 2)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    # Retorna o tipo do bloco funcional
    def getType(self):
        return self.item_type

    # Adiciona um conector a lista de conectores de entrada do bloco
    def addInputConnector(self, connector):
        self.input_connectors.append(connector)

    # Adiciona um conector a lista de conectores de saida do bloco
    def addOutputConnector(self, connector):
        self.output_connectors.append(connector)

    # Retorna a lista de conectores de entrada
    def getInputConnectors(self):
        return self.input_connectors

    # Remove um conector de entrada especifico da lista de conectores de entrada do bloco
    def removeInputConnector(self, connector):
        self.input_connectors.remove(connector)

    # Remove um conector de saida especifico da lista de conectores de saida do bloco
    def removeOutputConnector(self, connector):
        self.output_connectors.remove(connector)

