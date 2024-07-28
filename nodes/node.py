# Classe que representa os itens que podem ser desenhados no diagrama

# Podem ser:
#   * Blocos funcionais

# Deverá ser re-organizada com somente os parametros em comum de cada bloco para que possa ser herdada nas futuras classes
# que representarão cada bloco

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QFontMetrics, QPen, QBrush, QPainterPath, QFont
from PyQt5.QtCore import QRectF, QPointF, Qt, QSizeF
from PyQt5.QtSvg import QSvgRenderer
import numpy as np  # Para manipulação de matrizes

class Node(QGraphicsItem):

    def __init__(self, item_type, image_path):
        super().__init__()

        # Vai ser usando como retorno em alguns metodos
        self.item_type = item_type

        # Nome do bloco. É o nome que será renderizado abaixo do bloco
        self.item_name = item_type

        # Imagem do bloco funcional
        self.svg_renderer = QSvgRenderer(image_path)
        
        # Tamanho da imagem do bloco funcional
        self.width = 85
        self.height = 85

        # Tamanho do texto do bloco funcional
        self.font = QFont()
        self.font.setPointSize(8)

        # Altura em pixels do texto do bloco funcional
        self.text_height_in_pixels = 0

        # Listas que guardam a referencia dos conectores de entrada e saida do bloco funcional
        self.input_connectors = []
        self.output_connectors = []

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # Note que os seguintes atributos deverão ser re-organizados quando eu criar no futuro uma classe para cada bloco

        # Padrão de cor inicial para o bloco de carregar imagem
        self.color_pattern = "RGB"

        # Caminho para o arquivo da imagem
        self.image = None 

        # Kernel de convolução inicial para o bloco de kernel de convolução
        self.convolution_kernel = np.zeros((3, 3), dtype=np.float32)

        # Fator de divisibilidade inicial para o bloco de kernel de convolução
        self.divisibility = 1.0

    def paint(self, painter, option, widget):

        # Cor da caneta para escrever o texto abaixo do bloco
        painter.setPen(QPen(Qt.black))

        # Me pergunto se isso aqui é necessario
        painter.setBrush(QBrush(Qt.NoBrush))
        
        # Tamanho do texto abaixo do bloco
        painter.setFont(self.font)
        
        # Se o icone do bloco existe e foi lido corretamente
        if self.svg_renderer and self.svg_renderer.isValid():

            # Adquire o retangulo delimitador do bloco funcional
            image_rect = self.boundingRect()

            # Adquire o tamanho do retangulo delimitador e o converte para o tipo QSizeF
            image_size = QSizeF(image_rect.size())  

            # Adquire o tamanho padrão do icone utilizado pelo bloco
            size = self.svg_renderer.defaultSize()
            
            # Converte o padrão para o tipo QSizeF
            size = QSizeF(size) 

            # Ajusta o tamanho do icone para o tamanho do retangulo delimitador, mantendo a proporção entre altura e largura
            size.scale(image_size, Qt.KeepAspectRatio)

            # Define o tamanho do retangulo delimitador para o tamanho ajustado
            image_rect.setSize(size)

            # Renderiza o bloco
            self.svg_renderer.render(painter, image_rect)
            
            # Obtém a fonte atual usada pelo painter
            font = painter.font()
            
            # Cria um QFontMetrics para medir o tamanho do texto com a fonte atual
            fm = QFontMetrics(font)
            
            # Armazena a altura do texto em pixels na variável text_height_in_pixels
            self.text_height_in_pixels = fm.height()
            
            # Cria um retângulo que define a área onde o texto será desenhado
            text_rect = QRectF(0, 0, self.width, self.height)
            
            # Ajusta a altura do retângulo para incluir a altura do texto
            # Isso garante que o retângulo seja alto o suficiente para acomodar o bloco e o texto
            text_rect.setHeight(self.height + self.text_height_in_pixels)
            
            # Define a cor da caneta (pen) para desenhar o texto
            # Aqui está sendo definido como preto
            painter.setPen(QPen(Qt.black))
            
            # Desenha o texto no retângulo definido (text_rect)
            # O texto é alinhado no fundo e no centro horizontalmente
            painter.drawText(text_rect, Qt.AlignBottom | Qt.AlignHCenter, self.item_name)

        
        # Se o bloco funcional estiver selecionado, desenha uma borda ao redor dele
        if self.isSelected():
            painter.setPen(QPen(Qt.blue))
        else:
            # Caso contrário, remove a borda
            painter.setPen(QPen(Qt.transparent))
            
        # Define o pincel como nenhum e desenha o retângulo delimitador
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawRect(self.boundingRect())

        # Força a atualização do item para garantir que as mudanças sejam refletidas
        self.update()

    # Retorna o retangulo delimitador do bloco funcional
    # Esse é um metodo abstrato da classe QGraphicsItem e precisa ser implementado em todas as classes que herdam dela
    def boundingRect(self):

        # Retorna com um pequeno ajuste na altura para escrever o texto caso for um bloco que precise ter o texto escrito abaixo
        # Caso contrario retorna apenas o retangulo delimitador exato
        return QRectF(0, 0, self.width, self.height + self.text_height_in_pixels)
        # if self.item_type in ["Carregar Imagem", "Mostrar Imagem", "Kernel de Convolução", "Convolução"]:
        #     return QRectF(0, 0, self.width, self.height + self.text_height_in_pixels)
        # else:
        #     return QRectF(0, 0, self.width, self.height)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for connector in self.input_connectors:
                connector.updatePosition()
            for connector in self.output_connectors:
                connector.updatePosition()
        return super().itemChange(change, value)

    def center(self):
        return QPointF(self.x() + self.width / 2, self.y() + self.height / 2)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def getType(self):
        return self.item_type

    def numberOfConnections(self):
        return len(self.input_connectors)

    def addInputConnector(self, connector):
        self.input_connectors.append(connector)

    def addOutputConnector(self, connector):
        self.output_connectors.append(connector)

    def nInputs(self):
        return len(self.input_connectors)

    def getInputConnectors(self):
        return self.input_connectors

    def removeInputConnector(self, connector):
        self.input_connectors.remove(connector)

    def removeOutputConnector(self, connector):
        self.output_connectors.remove(connector)

    def getColorPattern(self):
        return self.color_pattern

    def setColorPattern(self, pattern):
        self.color_pattern = pattern

    def setMatrix(self, mat):
        self.convolution_kernel = np.array(mat, dtype=np.float32)

    def getMatrix(self):
        return self.convolution_kernel.tolist()

    def setDivisibility(self, div):
        self.divisibility = div

    def getDivisibility(self):
        return self.divisibility
    
    def setImage(self, image):
        self.image = image
